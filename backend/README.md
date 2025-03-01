# Shortify Backend

The backend API service for Shortify URL shortener, built with FastAPI, MongoDB, and Redis. This service provides high-performance URL shortening with real-time analytics and caching.

## Features

- ⚡️ **High-Performance URL Shortening**
  - Async operations with FastAPI
  - Redis caching for fast URL lookups
  - MongoDB for persistent storage

- 📊 **Real-time Analytics**
  - Click tracking with Redis counters
  - Background sync to MongoDB
  - Non-blocking click updates

- 🚀 **Production-Ready**
  - Comprehensive logging system
  - CORS support
  - Environment-based configuration
  - Graceful startup/shutdown

## Tech Stack

- Python 3.12+
- FastAPI with Pydantic
- MongoDB (with Motor async driver)
- Redis for caching
- uv for dependency management

## Quick Start

1. Set up environment:

   ```bash
   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate

   # Install dependencies using uv
   uv pip install .
   ```

2. Configure environment:

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

Visit `http://localhost:8000/docs` for interactive API documentation.

## Dependencies

Key dependencies from `pyproject.toml`:

```toml
dependencies = [
    "fastapi[standard]",
    "pymongo",
    "python-dotenv",
    "pydantic",
    "nanoid",
    "motor",
    "pydantic-settings>=2.8.1",
    "redis>=5.0.0",
]
```

## API Endpoints

### Create Shortened URL

```http
POST /api/shorten
Content-Type: application/json

{
    "target_url": "https://example.com/very-long-url"
}
```

### List All URLs

```http
GET /api/urls
```

### Get URL Details

```http
GET /api/urls/{url_id}
```

### Redirect to Original URL

```http
GET /{short_code}
```

## Configuration

Key environment variables:

```env
# Application Settings
PROJECT_NAME=shortify.tech
BASE_URL=http://localhost:8000

# MongoDB Settings
MONGODB_URL=mongodb://localhost:27017
DB_NAME=shortify

# Redis Settings
REDIS_URL=redis://localhost:6379
REDIS_CACHE_TTL=3600
REDIS_CLICK_SYNC_INTERVAL=60

# Security Settings
CORS_ORIGINS=["http://localhost:3000"]
RATE_LIMIT_PER_MINUTE=60
```

## Project Structure

```
backend/
├── app/
│   ├── api/        # API routes & endpoints
│   ├── core/       # Core functionality
│   ├── db/         # Database clients
│   └── models/     # Pydantic models
├── pyproject.toml  # Project metadata and dependencies
└── main.py         # Application entry point
```

### Key Components

- `app/api/routes.py`: API endpoint definitions
- `app/core/shortener.py`: URL shortening logic
- `app/db/mongodb.py`: MongoDB connection and operations
- `app/db/redis.py`: Redis caching layer
- `app/models/url.py`: Data models and schemas

## Development

### Code Style

Follow these guidelines:

- Use type hints
- Follow PEP 8 standards
- Maximum line length: 88 characters (Black default)

### Testing

```bash
# Run tests
pytest

# Code formatting
black .
isort .
```

## Performance Considerations

1. **Caching Strategy**
   - URLs cached in Redis for fast lookups
   - Click counts buffered in Redis
   - Periodic synchronization to MongoDB

2. **Background Tasks**
   - Asynchronous click tracking
   - Non-blocking cache updates
   - Scheduled database synchronization

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

See the root [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.
