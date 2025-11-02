from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import praw
from textblob import TextBlob
from datetime import datetime, timedelta
import sqlite3
import json
from collections import Counter
import re

app = FastAPI(title="Sentiment Analyzer API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
def init_db():
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  platform TEXT,
                  author TEXT,
                  text TEXT,
                  sentiment TEXT,
                  score REAL,
                  timestamp TEXT,
                  keyword TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Pydantic models
class AnalyzeRequest(BaseModel):
    keyword: str
    platform: str = "reddit"
    timeframe: str = "24h"
    limit: int = 100

class PostResponse(BaseModel):
    author: str
    text: str
    sentiment: str
    score: float
    time: str
    platform: str

# Reddit API setup (Replace with your credentials)
# Get from: https://www.reddit.com/prefs/apps
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="sentiment_analyzer:v1.0"
)

# Sentiment analysis function
def analyze_sentiment(text: str) -> tuple:
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return sentiment, polarity

# Extract keywords/hashtags
def extract_keywords(text: str) -> List[str]:
    """Extract hashtags and important words"""
    hashtags = re.findall(r'#\w+', text.lower())
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    return hashtags + words

# Background task for data collection
def collect_reddit_data(keyword: str, limit: int):
    """Collect posts from Reddit and analyze sentiment"""
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    
    posts_collected = 0
    
    try:
        # Try multiple search strategies
        subreddit = reddit.subreddit("all")
        
        # Strategy 1: Search with different time filters
        time_filters = ['day', 'week', 'month']
        
        for time_filter in time_filters:
            if posts_collected >= limit:
                break
                
            try:
                posts = subreddit.search(keyword, limit=limit-posts_collected, time_filter=time_filter)
                
                for post in posts:
                    if posts_collected >= limit:
                        break
                        
                    text = f"{post.title} {post.selftext}"
                    
                    # Skip if too short
                    if len(text.strip()) < 10:
                        continue
                    
                    sentiment, score = analyze_sentiment(text)
                    
                    c.execute('''INSERT INTO posts 
                                (platform, author, text, sentiment, score, timestamp, keyword)
                                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                             ('reddit', str(post.author), text[:500], sentiment, 
                              score, datetime.now().isoformat(), keyword.lower()))
                    
                    posts_collected += 1
                
                conn.commit()
                print(f"Collected {posts_collected} posts for '{keyword}' with time_filter={time_filter}")
                
            except Exception as e:
                print(f"Error with time_filter {time_filter}: {e}")
                continue
        
        # Strategy 2: If still no posts, try specific subreddits
        if posts_collected == 0:
            # Map keywords to relevant subreddits
            keyword_subreddits = {
                'car': ['cars', 'autos', 'automotive'],
                'bb': ['basketball', 'nba'],
                'tesla': ['teslamotors', 'electricvehicles'],
                'gaming': ['gaming', 'games'],
                'tech': ['technology', 'tech'],
                'food': ['food', 'cooking'],
            }
            
            relevant_subs = keyword_subreddits.get(keyword.lower(), ['popular', 'AskReddit'])
            
            for sub_name in relevant_subs[:2]:
                if posts_collected >= limit:
                    break
                try:
                    sub = reddit.subreddit(sub_name)
                    for post in sub.hot(limit=20):
                        if posts_collected >= limit:
                            break
                        
                        text = f"{post.title} {post.selftext}"
                        
                        # Check if keyword is in the post
                        if keyword.lower() not in text.lower():
                            continue
                        
                        sentiment, score = analyze_sentiment(text)
                        
                        c.execute('''INSERT INTO posts 
                                    (platform, author, text, sentiment, score, timestamp, keyword)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                 ('reddit', str(post.author), text[:500], sentiment, 
                                  score, datetime.now().isoformat(), keyword.lower()))
                        
                        posts_collected += 1
                    
                    conn.commit()
                    print(f"Collected {posts_collected} posts from r/{sub_name}")
                except Exception as e:
                    print(f"Error with subreddit {sub_name}: {e}")
        
        print(f"Total collected for '{keyword}': {posts_collected} posts")
        
    except Exception as e:
        print(f"Error collecting data: {e}")
    finally:
        conn.close()
    
    return posts_collected

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Sentiment Analyzer API", "status": "running"}

@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    """Trigger sentiment analysis for a keyword"""
    keyword = request.keyword.strip().lower()
    
    # Check if we already have recent data for this keyword
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    c.execute("""SELECT COUNT(*) FROM posts 
                 WHERE LOWER(keyword) = ? 
                 AND datetime(timestamp) > datetime('now', '-1 hour')""", (keyword,))
    recent_count = c.fetchone()[0]
    conn.close()
    
    if recent_count > 0:
        return {
            "status": "cached",
            "message": f"Using existing data for '{keyword}' ({recent_count} posts). Click Refresh to see it.",
            "keyword": keyword,
            "count": recent_count
        }
    
    background_tasks.add_task(collect_reddit_data, keyword, request.limit)
    return {
        "status": "started",
        "message": f"Collecting posts for '{keyword}'. This may take 10-30 seconds. Click Refresh after waiting.",
        "keyword": keyword
    }

@app.get("/api/stats")
async def get_stats(keyword: Optional[str] = None):
    """Get sentiment statistics"""
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    
    if keyword and keyword.strip():
        # Use LIKE for partial matching
        c.execute("SELECT sentiment FROM posts WHERE LOWER(keyword) = LOWER(?)", (keyword.strip(),))
    else:
        c.execute("SELECT sentiment FROM posts")
    
    results = c.fetchall()
    conn.close()
    
    if not results:
        return {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "positive_pct": 0,
            "negative_pct": 0,
            "neutral_pct": 0,
            "keyword": keyword
        }
    
    sentiments = [r[0] for r in results]
    counter = Counter(sentiments)
    total = len(sentiments)
    
    return {
        "total": total,
        "positive": counter.get('positive', 0),
        "negative": counter.get('negative', 0),
        "neutral": counter.get('neutral', 0),
        "positive_pct": round(counter.get('positive', 0) / total * 100, 1) if total > 0 else 0,
        "negative_pct": round(counter.get('negative', 0) / total * 100, 1) if total > 0 else 0,
        "neutral_pct": round(counter.get('neutral', 0) / total * 100, 1) if total > 0 else 0,
        "keyword": keyword
    }

@app.get("/api/posts")
async def get_posts(limit: int = 20, keyword: Optional[str] = None):
    """Get recent analyzed posts"""
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    
    if keyword and keyword.strip():
        c.execute("""SELECT platform, author, text, sentiment, score, timestamp, keyword
                    FROM posts WHERE LOWER(keyword) = LOWER(?)
                    ORDER BY timestamp DESC LIMIT ?""", (keyword.strip(), limit))
    else:
        c.execute("""SELECT platform, author, text, sentiment, score, timestamp, keyword
                    FROM posts ORDER BY timestamp DESC LIMIT ?""", (limit,))
    
    results = c.fetchall()
    conn.close()
    
    posts = []
    for r in results:
        try:
            time_diff = datetime.now() - datetime.fromisoformat(r[5])
            hours = int(time_diff.total_seconds() / 3600)
            if hours < 1:
                time_str = "Just now"
            elif hours < 24:
                time_str = f"{hours} hours ago"
            else:
                days = hours // 24
                time_str = f"{days} days ago"
        except:
            time_str = "Unknown"
        
        posts.append({
            "platform": r[0],
            "author": r[1],
            "text": r[2][:200],
            "sentiment": r[3],
            "score": round(r[4], 2),
            "time": time_str,
            "keyword": r[6] if len(r) > 6 else ""
        })
    
    return {"posts": posts, "count": len(posts), "keyword": keyword}

@app.get("/api/trends")
async def get_trends(keyword: Optional[str] = None, limit: int = 10):
    """Get trending keywords and hashtags"""
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    
    if keyword and keyword.strip():
        c.execute("SELECT text FROM posts WHERE LOWER(keyword) = LOWER(?)", (keyword.strip(),))
    else:
        c.execute("SELECT text FROM posts")
    
    results = c.fetchall()
    conn.close()
    
    all_keywords = []
    for r in results:
        all_keywords.extend(extract_keywords(r[0]))
    
    common = Counter(all_keywords).most_common(limit)
    
    return {
        "trends": [{"keyword": k, "count": c} for k, c in common],
        "total": len(all_keywords)
    }

@app.get("/api/timeline")
async def get_timeline(keyword: Optional[str] = None):
    """Get sentiment over time"""
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    
    if keyword and keyword.strip():
        c.execute("""SELECT sentiment, timestamp FROM posts 
                    WHERE LOWER(keyword) = LOWER(?)
                    ORDER BY timestamp""", (keyword.strip(),))
    else:
        c.execute("SELECT sentiment, timestamp FROM posts ORDER BY timestamp")
    
    results = c.fetchall()
    conn.close()
    
    # Group by day
    timeline = {}
    for sentiment, timestamp in results:
        try:
            date = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d')
            if date not in timeline:
                timeline[date] = {'positive': 0, 'negative': 0, 'neutral': 0}
            timeline[date][sentiment] += 1
        except:
            continue
    
    return {"timeline": timeline, "keyword": keyword}

@app.delete("/api/clear")
async def clear_data():
    """Clear all data from database"""
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    c.execute("DELETE FROM posts")
    conn.commit()
    conn.close()
    return {"message": "All data cleared"}

@app.get("/api/debug/keywords")
async def debug_keywords():
    """Debug endpoint to see all stored keywords"""
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT keyword, COUNT(*) as count FROM posts GROUP BY keyword")
    results = c.fetchall()
    conn.close()
    return {
        "stored_keywords": [{"keyword": r[0], "count": r[1]} for r in results],
        "total_keywords": len(results)
    }

@app.get("/api/status/{keyword}")
async def get_status(keyword: str):
    """Check if data exists for a keyword"""
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM posts WHERE LOWER(keyword) = LOWER(?)", (keyword.strip(),))
    count = c.fetchone()[0]
    
    c.execute("""SELECT MAX(timestamp) FROM posts 
                 WHERE LOWER(keyword) = LOWER(?)""", (keyword.strip(),))
    last_update = c.fetchone()[0]
    
    conn.close()
    
    return {
        "keyword": keyword,
        "exists": count > 0,
        "count": count,
        "last_update": last_update
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)