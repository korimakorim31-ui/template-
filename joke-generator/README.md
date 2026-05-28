# Random Joke Generator API

A simple yet powerful API application that generates random jokes using external APIs. Built with FastAPI and integrated with multiple joke providers.

## 🎯 Features

- **Random Joke Generation** - Get random jokes instantly
- **Multiple Joke Types** - General, Programming, Knock-knock, Dad jokes
- **Multiple API Providers** - JokeAPI, Official Jokes API, and more
- **Caching** - Smart caching to reduce API calls
- **Rate Limiting** - Protect against abuse
- **Search Functionality** - Search jokes by keyword
- **Filtering** - Filter jokes by type and category
- **Translation** - Multi-language support
- **User Ratings** - Rate and save favorite jokes
- **REST API** - Full API documentation with Swagger UI
- **WebSocket Support** - Real-time joke streaming

## 📋 Requirements

- Python 3.10+
- FastAPI
- httpx (async HTTP client)
- SQLAlchemy (for database)
- Redis (for caching)

## 🚀 Quick Start

### 1. Installation

```bash
cd joke-generator
pip install -r requirements.txt
```

### 2. Configuration

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
DEBUG=True
APP_PORT=8001
REDIS_URL=redis://localhost:6379/0
JOKE_CACHE_TTL=3600
```

### 3. Run the Application

```bash
uvicorn app.main:app --reload --port 8001
```

Visit: `http://localhost:8001/docs`

## 📚 API Endpoints

### Get Random Joke
```bash
GET /api/jokes/random
```

**Response:**
```json
{
  "id": 1,
  "joke": "Why don't scientists trust atoms? Because they make up everything!",
  "type": "general",
  "category": "science",
  "source": "jokeapi",
  "rating": 4.5,
  "saved": false
}
```

### Get Joke by Type
```bash
GET /api/jokes/random?type=programming
```

**Supported Types:**
- `general` - General jokes
- `programming` - Programming jokes
- `knock-knock` - Knock-knock jokes
- `dad` - Dad jokes
- `science` - Science jokes
- `sports` - Sports jokes

### Search Jokes
```bash
GET /api/jokes/search?keyword=python
```

### Get Joke by ID
```bash
GET /api/jokes/{joke_id}
```

### Rate a Joke
```bash
POST /api/jokes/{joke_id}/rate

{
  "rating": 5
}
```

### Save Favorite Joke
```bash
POST /api/jokes/{joke_id}/favorite
```

### Get Favorite Jokes
```bash
GET /api/jokes/favorites
```

### Translate Joke
```bash
POST /api/jokes/{joke_id}/translate

{
  "target_language": "es"
}
```

### WebSocket - Stream Jokes
```bash
WebSocket /ws/jokes/stream
```

## 🎲 Random Endpoints

### Get Multiple Random Jokes
```bash
GET /api/jokes/random/batch?count=5
```

### Get Joke Without Specific Words
```bash
GET /api/jokes/random?exclude_words=politics,religion
```

## 📊 Statistics

```bash
GET /api/stats/jokes
```

**Response:**
```json
{
  "total_jokes": 1250,
  "total_ratings": 453,
  "average_rating": 4.2,
  "by_type": {
    "general": 450,
    "programming": 300,
    "knock-knock": 200,
    "dad": 300
  },
  "most_rated": "Why do programmers like dark mode?",
  "highest_rated": "Why don't scientists trust atoms?"
}
```

## 🔧 External APIs Used

### 1. JokeAPI
- **URL:** `https://jokeapi.dev/api/joke/
`
- **Features:** Multiple joke categories, safe/unsafe mode, blacklist words
- **Rate Limit:** 120 requests per minute

### 2. Official Jokes API
- **URL:** `https://official-joke-api.appspot.com/
`
- **Features:** General jokes, programming jokes, knock-knock jokes
- **Rate Limit:** No strict limit

### 3. QuoteGarden (Bonus)
- **URL:** `https://quote-garden.herokuapp.com/api/v3/
`
- **Features:** Inspirational quotes

## 💾 Database Schema

### Jokes Table
```sql
CREATE TABLE jokes (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    type VARCHAR(50),
    category VARCHAR(50),
    source VARCHAR(50),
    setup TEXT,
    delivery TEXT,
    rating FLOAT DEFAULT 0,
    rating_count INTEGER DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME
);
```

### User Ratings Table
```sql
CREATE TABLE joke_ratings (
    id INTEGER PRIMARY KEY,
    joke_id INTEGER,
    user_id VARCHAR(100),
    rating INTEGER,
    created_at DATETIME
);
```

### Favorites Table
```sql
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY,
    joke_id INTEGER,
    user_id VARCHAR(100),
    created_at DATETIME
);
```

## 🚀 Deployment

### Docker

```bash
cd joke-generator
docker build -t joke-generator .
docker run -p 8001:8001 joke-generator
```

### Docker Compose

```bash
docker-compose up -d
```

## 📝 Example Usage

### Python

```python
import httpx
import asyncio

async def get_random_joke():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8001/api/jokes/random?type=programming"
        )
        joke = response.json()
        print(f"Joke: {joke['joke']}")
        print(f"Rating: {joke['rating']}")

asyncio.run(get_random_joke())
```

### JavaScript/Node.js

```javascript
const fetchJoke = async () => {
  const response = await fetch(
    'http://localhost:8001/api/jokes/random?type=dad'
  );
  const joke = await response.json();
  console.log(`Joke: ${joke.joke}`);
  console.log(`Rating: ${joke.rating}`);
};

fetchJoke();
```

### cURL

```bash
# Get random joke
curl http://localhost:8001/api/jokes/random

# Get programming joke
curl "http://localhost:8001/api/jokes/random?type=programming"

# Search jokes
curl "http://localhost:8001/api/jokes/search?keyword=python"

# Rate a joke
curl -X POST http://localhost:8001/api/jokes/1/rate \
  -H "Content-Type: application/json" \
  -d '{"rating": 5}'
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_jokes.py
```

## 📦 Project Structure

```
joke-generator/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── database.py             # Database setup
│   ├── models/
│   │   ├── joke.py             # Joke model
│   │   ├── rating.py           # Rating model
│   │   └── favorite.py         # Favorite model
│   ├── api/
│   │   ├── jokes.py            # Joke endpoints
│   │   ├── ratings.py          # Rating endpoints
│   │   └── stats.py            # Statistics endpoints
│   ├── services/
│   │   ├── joke_service.py     # Joke business logic
│   │   ├── cache_service.py    # Caching logic
│   │   └── external_api.py     # External API calls
│   └── utils/
│       └── logger.py           # Logging setup
├── tests/
│   └── test_jokes.py           # Unit tests
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
├── Dockerfile                  # Docker config
├── docker-compose.yml          # Docker Compose
└── README.md                   # This file
```

## 🛠️ Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | False | Debug mode |
| `APP_PORT` | 8001 | Application port |
| `REDIS_URL` | redis://localhost:6379/0 | Redis connection |
| `JOKE_CACHE_TTL` | 3600 | Cache TTL in seconds |
| `RATE_LIMIT_REQUESTS` | 100 | Requests per period |
| `RATE_LIMIT_PERIOD` | 3600 | Rate limit period in seconds |
| `DATABASE_URL` | sqlite:///jokes.db | Database URL |

## 🔒 Security

- Rate limiting on all endpoints
- Input validation and sanitization
- CORS configuration
- SQL injection prevention with ORM
- XSS protection

## 📄 License

MIT License - Free to use and modify

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please create a GitHub issue.

---

**Made with ❤️ for joke enthusiasts**
