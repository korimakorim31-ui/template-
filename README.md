# AI Crypto KOL Writer Bot

An advanced AI-powered bot designed for cryptocurrency influencers and content creators to generate, rewrite, and optimize social media content. Built with Python, FastAPI, and OpenAI/Claude APIs.

## 🚀 Features

- **Tweet Generation**: Create engaging tweets from scratch using AI
- **Tweet Rewriting**: Transform viral tweets for your audience
- **Auto Hashtag Addition**: Automatically add relevant hashtags
- **Multi-Language Support**: Generate content in multiple languages
- **Learning from Styles**: Learn from your uploaded tweet styles
- **Auto CTA**: Automatic call-to-action generation for engagement
- **Thread Generator**: Create engaging tweet threads
- **Meme Caption Generator**: Generate captions for memes with Telegram bot integration
- **Dashboard**: Web-based admin panel
- **API**: RESTful API for integrations

## 📋 Requirements

- Python 3.10+
- PostgreSQL/SQLite
- OpenAI API Key or Anthropic Claude API Key
- Telegram Bot Token (for meme caption generator)
- Twitter API credentials (optional, for direct posting)

## 🔧 Installation

### 1. Clone Repository
```bash
git clone https://github.com/korimakorim31-ui/template-.git
cd template-
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Database Setup
```bash
python scripts/init_db.py
```

### 6. Run Application
```bash
# API Server
uvicorn app.main:app --reload

# Telegram Bot (separate terminal)
python app/telegram_bot/bot.py

# Celery Worker (for background tasks)
celery -A app.celery worker --loglevel=info
```

## 📖 API Documentation

Once running, visit: `http://localhost:8000/docs`

## 🗂️ Project Structure

```
template-/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database setup
│   ├── models/                 # Pydantic models
│   ├── api/                    # API routes
│   ├── services/               # Business logic
│   ├── ml/                     # ML/AI features
│   ├── telegram_bot/           # Telegram bot integration
│   └── utils/                  # Utility functions
├── web/                        # Frontend dashboard
├── scripts/                    # Setup and utility scripts
├── tests/                      # Unit and integration tests
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── docker-compose.yml          # Docker configuration
└── README.md                   # This file
```

## 🔑 API Endpoints

### Tweet Management
- `POST /api/tweets/generate` - Generate a new tweet
- `POST /api/tweets/rewrite` - Rewrite an existing tweet
- `POST /api/tweets/add-hashtags` - Add hashtags to tweet
- `POST /api/tweets/thread` - Generate a tweet thread
- `GET /api/tweets/{id}` - Get tweet details
- `DELETE /api/tweets/{id}` - Delete a tweet

### Style Learning
- `POST /api/styles/upload` - Upload tweet styles for learning
- `GET /api/styles` - List learned styles
- `DELETE /api/styles/{id}` - Delete a style

### Multi-Language
- `POST /api/tweets/translate` - Translate content to other languages
- `GET /api/languages` - Supported languages

### Meme Generation
- `POST /api/memes/caption` - Generate meme caption
- `GET /api/memes/{id}` - Get meme details

## 🤖 Example Usage

### Generate Tweet
```bash
curl -X POST http://localhost:8000/api/tweets/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Bitcoin",
    "tone": "bullish",
    "language": "en",
    "include_cta": true
  }'
```

### Rewrite Tweet
```bash
curl -X POST http://localhost:8000/api/tweets/rewrite \
  -H "Content-Type: application/json" \
  -d '{
    "original_tweet": "Bitcoin is going up!",
    "style": "formal",
    "language": "en"
  }'
```

### Generate Thread
```bash
curl -X POST http://localhost:8000/api/tweets/thread \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "DeFi Trends",
    "thread_length": 5,
    "language": "en"
  }'
```

## 🧠 AI Models

The bot supports multiple AI backends:

1. **OpenAI GPT-4** (Default)
   - Best for quality and speed
   - Set `AI_PROVIDER=openai` in .env

2. **Anthropic Claude 3**
   - Better for nuanced content
   - Set `AI_PROVIDER=anthropic` in .env

3. **Open Source Models** (Llama, Mistral)
   - Self-hosted option
   - Set `AI_PROVIDER=ollama` in .env

## 💾 Database Schema

- **Users** - User accounts and API keys
- **Tweets** - Generated and stored tweets
- **TweetStyles** - Learned tweet writing styles
- **Hashtags** - Hashtag database and frequency
- **Memes** - Generated meme captions
- **Languages** - Supported languages and translations

## 🔐 Security

- API key authentication
- Rate limiting (100 requests/hour per user)
- Input sanitization
- CORS configuration
- Environment variables for secrets
- JWT tokens for session management

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_tweet_generation.py
```

## 📦 Deployment

### Docker
```bash
docker-compose up -d
```

### Heroku
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### AWS/GCP
See `deployment/` directory for cloud-specific configs.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- GitHub Issues: [Create an issue](https://github.com/korimakorim31-ui/template-/issues)
- Documentation: [Wiki](https://github.com/korimakorim31-ui/template-/wiki)
- Email: support@aiwriter.bot

## 🗺️ Roadmap

- [ ] TikTok/Instagram caption generation
- [ ] LinkedIn article writer
- [ ] YouTube video title/description generator
- [ ] Email marketing copy
- [ ] A/B testing framework
- [ ] Analytics dashboard
- [ ] Browser extension
- [ ] Mobile app

---

**Made with ❤️ for Crypto KOLs**
