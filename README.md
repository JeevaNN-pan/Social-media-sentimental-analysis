# 🎭 Social Media Sentiment Analyzer

A full-stack web application that performs real-time sentiment analysis on social media posts using AI and natural language processing. Analyze trends, track sentiment patterns, and gain insights from Reddit discussions.


## 📸 Features Overview

*A comprehensive sentiment analysis platform analyzing social media discussions in real-time.*

## ✨ Features

### Current Features
- ✅ **Real-time Data Collection**: Fetches posts from Reddit using PRAW API
- ✅ **AI Sentiment Analysis**: Analyzes sentiment using TextBlob NLP library
- ✅ **Interactive Dashboard**: Modern, responsive UI with real-time charts
- ✅ **Multiple Search Strategies**: Searches across time periods and relevant subreddits
- ✅ **Keyword Tracking**: Track sentiment for any keyword or topic
- ✅ **Trending Topics**: Discover trending keywords and hashtags
- ✅ **Historical Analysis**: View sentiment trends over time
- ✅ **RESTful API**: Well-documented API endpoints for data access
- ✅ **Debug Tools**: Built-in debugging panel for troubleshooting

### 📊 Analytics Provided
- Sentiment distribution (Positive/Neutral/Negative percentages)
- Sentiment timeline visualization
- Trending keywords and hashtags
- Recent posts with sentiment scores
- Platform-wise breakdown

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.8+)
- **NLP**: TextBlob for sentiment analysis
- **Reddit API**: PRAW (Python Reddit API Wrapper)
- **Database**: SQLite3
- **Background Tasks**: Celery-style async processing with FastAPI BackgroundTasks
- **Web Server**: Uvicorn (ASGI server)

### Frontend
- **HTML5/CSS3**: Responsive design
- **JavaScript**: Vanilla JS with Fetch API
- **Visualization**: Chart.js for interactive charts
- **UI Design**: Modern gradient design with smooth animations

### APIs & Libraries
- Reddit API (PRAW)
- TextBlob for NLP
- Chart.js for data visualization

## 📋 Prerequisites

- Python 3.8 or higher
- Reddit API credentials (free)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/jeevanpanda1234/sentiment-analyzer.git
cd sentiment-analyzer
```

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt

# Download TextBlob corpora
python -m textblob.download_corpora
```

### Step 4: Get Reddit API Credentials

1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **"Create App"** or **"Create Another App"**
3. Fill in the details:
   - **Name**: Sentiment Analyzer
   - **App type**: Choose **"script"**
   - **Description**: Sentiment analysis tool
   - **About URL**: Leave blank
   - **Redirect URI**: `http://localhost:8000`
4. Click **"Create app"**
5. Copy your **client_id** (under the app name) and **client_secret**

### Step 5: Configure API Credentials

Open `backend/app.py` and update:

```python
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID_HERE",
    client_secret="YOUR_CLIENT_SECRET_HERE",
    user_agent="sentiment_analyzer:v1.0"
)
```

### Step 6: Run the Application

```bash
# Start backend server
cd backend
python app.py

# Backend will run at: http://localhost:8000
```

Open `frontend/index.html` in your web browser.

## 💻 Usage

### Basic Workflow

1. **Enter a keyword** in the search box (e.g., "python", "gaming", "bitcoin")
2. **Click "Analyze"** to start collecting posts from Reddit
3. **Wait 15-20 seconds** for data collection (auto-refreshes)
4. **View results**:
   - Sentiment statistics (positive/negative/neutral counts)
   - Interactive charts and visualizations
   - Recent posts with sentiment scores
   - Trending keywords

### Recommended Keywords

**Popular Topics** (Always work well):
- `python`, `javascript`, `programming`
- `gaming`, `movies`, `music`
- `technology`, `AI`, `machine learning`
- `bitcoin`, `crypto`, `stocks`
- `climate`, `science`, `space`

**Specific Topics** (May have fewer results):
- `tesla`, `apple`, `google`
- `basketball`, `football`, `sports`
- `food`, `cooking`, `recipes`
- `travel`, `photography`, `art`

### Tips for Best Results
- Use popular, trending topics
- Avoid very short keywords (2 letters)
- Use specific terms rather than generic ones
- Keywords are case-insensitive
- Wait for auto-refresh after clicking Analyze

## 🌐 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Analyze Keyword
```http
POST /api/analyze
Content-Type: application/json

{
  "keyword": "python",
  "platform": "reddit",
  "timeframe": "24h",
  "limit": 50
}
```

**Response:**
```json
{
  "status": "started",
  "message": "Collecting posts for 'python'...",
  "keyword": "python"
}
```

#### 2. Get Sentiment Statistics
```http
GET /api/stats?keyword=python
```

**Response:**
```json
{
  "total": 50,
  "positive": 32,
  "negative": 8,
  "neutral": 10,
  "positive_pct": 64.0,
  "negative_pct": 16.0,
  "neutral_pct": 20.0,
  "keyword": "python"
}
```

#### 3. Get Recent Posts
```http
GET /api/posts?keyword=python&limit=20
```

**Response:**
```json
{
  "posts": [
    {
      "platform": "reddit",
      "author": "user123",
      "text": "Python is amazing for data science...",
      "sentiment": "positive",
      "score": 0.85,
      "time": "2 hours ago"
    }
  ],
  "count": 20
}
```

#### 4. Get Trending Keywords
```http
GET /api/trends?keyword=python&limit=10
```

#### 5. Get Sentiment Timeline
```http
GET /api/timeline?keyword=python
```

#### 6. Check Keyword Status
```http
GET /api/status/python
```

#### 7. Clear Database
```http
DELETE /api/clear
```

#### 8. Debug Endpoints
```http
GET /api/debug/keywords
GET /api/debug/all
```

## 📁 Project Structure

```
sentiment-analyzer/
├── backend/
│   ├── app.py                 # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── sentiment.db          # SQLite database (auto-created)
├── frontend/
│   └── index.html            # Dashboard UI
├── README.md                 # This file
└── .gitignore
```

## 🔧 Configuration

### Database Schema

```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT,
    author TEXT,
    text TEXT,
    sentiment TEXT,
    score REAL,
    timestamp TEXT,
    keyword TEXT
);
```

### Environment Variables (Optional)

You can set these in a `.env` file:

```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
DATABASE_URL=sqlite:///sentiment.db
API_PORT=8000
```

## 🧪 Testing

### Manual Testing

1. **Test Backend API**:
```bash
# Check if server is running
curl http://localhost:8000/

# Test analyze endpoint
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"keyword": "python", "limit": 10}'

# Check stats
curl http://localhost:8000/api/stats?keyword=python
```

2. **Test Frontend**:
- Open browser console (F12)
- Click "Debug" button to see stored data
- Try different keywords and verify different results

### Debug Mode

Click the **"🐛 Debug"** button in the UI to see:
- All stored keywords
- Post counts per keyword
- Sentiment breakdown
- Current keyword being queried

## 🐛 Troubleshooting

### Issue: "Error connecting to backend"
**Solution**: 
- Ensure backend is running: `python app.py`
- Check if port 8000 is available
- Verify no firewall blocking

### Issue: "No posts found for keyword"
**Solution**:
- Try more popular keywords
- Check backend terminal for errors
- Verify Reddit API credentials
- Try different keywords (gaming, python, bitcoin)

### Issue: Keywords showing same results
**Solution**:
- Click "Debug" button to verify data
- Make sure keywords are different
- Clear cache: `DELETE http://localhost:8000/api/clear`
- Restart backend server

### Issue: Reddit API Rate Limit
**Solution**:
- Wait a few minutes between analyses
- Reddit allows ~60 requests per minute
- The app implements smart caching

### Issue: Sentiment seems incorrect
**Solution**:
- TextBlob is rule-based, not perfect
- Consider upgrading to transformer models (future)
- Sarcasm and context can confuse simple NLP

## 🚀 Future Enhancements

### Planned Features (Roadmap)

#### Phase 1: Enhanced Analysis
- [ ] **Advanced NLP Models**: Integrate BERT/DistilBERT for better accuracy
- [ ] **Multi-language Support**: Analyze posts in different languages
- [ ] **Emotion Detection**: Beyond positive/negative (joy, anger, fear, etc.)
- [ ] **Topic Modeling**: Automatic topic extraction using LDA
- [ ] **Aspect-Based Sentiment**: Analyze sentiment for specific aspects

#### Phase 2: More Data Sources
- [ ] **Twitter/X Integration**: Add Twitter API support
- [ ] **News API**: Analyze news article sentiment
- [ ] **YouTube Comments**: Sentiment from video comments
- [ ] **Instagram**: Public post analysis
- [ ] **Custom Data Upload**: CSV/JSON file upload

#### Phase 3: Advanced Features
- [ ] **Real-time Streaming**: WebSocket for live updates
- [ ] **Comparative Analysis**: Compare sentiment across multiple keywords
- [ ] **Sentiment Alerts**: Email/SMS notifications for sentiment changes
- [ ] **Export Reports**: PDF/Excel reports generation
- [ ] **Historical Tracking**: Long-term sentiment tracking
- [ ] **Predictive Analysis**: Forecast sentiment trends

#### Phase 4: User Experience
- [ ] **User Authentication**: Multi-user support with JWT
- [ ] **Saved Searches**: Save and revisit keyword analyses
- [ ] **Custom Dashboards**: Personalized dashboard layouts
- [ ] **Mobile App**: React Native mobile application
- [ ] **Dark Mode**: UI theme toggle
- [ ] **Accessibility**: WCAG 2.1 compliance

#### Phase 5: Infrastructure
- [ ] **PostgreSQL Migration**: Scale to production database
- [ ] **Redis Caching**: Improve performance
- [ ] **Docker Deployment**: Containerized application
- [ ] **Cloud Deployment**: AWS/GCP/Azure deployment guides
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **API Rate Limiting**: Implement rate limiting
- [ ] **Monitoring**: Grafana/Prometheus integration

#### Phase 6: Machine Learning
- [ ] **Custom ML Models**: Train on domain-specific data
- [ ] **Transfer Learning**: Fine-tune pre-trained models
- [ ] **Active Learning**: Improve model with user feedback
- [ ] **A/B Testing**: Compare different models
- [ ] **Model Versioning**: Track model performance over time

### Technology Upgrades
- [ ] Migrate to React/Vue.js frontend
- [ ] Add TypeScript for type safety
- [ ] Implement GraphQL API
- [ ] Add Elasticsearch for better search
- [ ] Kubernetes orchestration

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Make your changes**
4. **Commit your changes**:
   ```bash
   git commit -m "Add some AmazingFeature"
   ```
5. **Push to the branch**:
   ```bash
   git push origin feature/AmazingFeature
   ```
6. **Open a Pull Request**

### Contribution Guidelines
- Follow PEP 8 style guide for Python code
- Write clear commit messages
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly
- Update README if needed

### Areas for Contribution
- Bug fixes
- New features from roadmap
- Documentation improvements
- UI/UX enhancements
- Performance optimizations
- Test coverage

## 👤 Author

**Jeevan**
- GitHub: [@jeevanpanda1234](https://github.com/jeevanpanda1234)
- Email: jeevanpanda1234@gmail.com

## 🙏 Acknowledgments

- **Reddit** for providing the PRAW API
- **TextBlob** for NLP capabilities
- **FastAPI** for the excellent web framework
- **Chart.js** for beautiful visualizations
- **The Open Source Community** for inspiration and tools

## 📚 Resources & References

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PRAW Documentation](https://praw.readthedocs.io/)
- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

### Tutorials Used
- Sentiment Analysis with Python
- Reddit API Best Practices
- FastAPI Background Tasks
- Frontend Data Visualization

## 📊 Project Stats

- **Version**: 1.0.0
- **Last Updated**: November 2024
- **Development Time**: 1 month
- **Lines of Code**: ~800+
- **Dependencies**: 6 core libraries


## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ and Python**

*Happy Analyzing! 🎭📊*
