# Real Estate Scraper API

A Django-based REST API for real estate property management with integrated web scraping capabilities.

## Quick Start

### 1. Run with Docker Compose
```bash
docker compose up
```

The API will be available at `http://localhost:8000`

### 2. Access API Documentation
Open your browser and go to:
- **Interactive API Docs**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### 3. Test the APIs
Use the interactive documentation or test with curl:

```bash
# Create a user
curl -X POST "http://localhost:8000/api/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "email": "test@example.com"}'

# Login and get token
curl -X POST "http://localhost:8000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# Use token for authenticated requests
curl -X GET "http://localhost:8000/api/properties/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Project Overview

### What It Does
- **Property Management**: CRUD operations for real estate properties
- **Web Scraping**: Integrated bot system for scraping property data
- **Data Export**: CSV export functionality for property data
- **User Authentication**: JWT-based authentication system
- **API Documentation**: Auto-generated OpenAPI 3.0 documentation

### Key Features
- **RESTful API**: Full CRUD operations for properties
- **Scraper Integration**: Run property scrapers via API or command line
- **Data Mapping**: Automatic mapping between scraper output and database models
- **Filtering**: Advanced property filtering (price, location, bedrooms, etc.)
- **Export**: Download property data in CSV format
- **Admin Interface**: Django admin for data management

### Architecture
- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL (via Docker)
- **Authentication**: JWT tokens
- **Documentation**: drf-spectacular (OpenAPI 3.0)
- **Containerization**: Docker + Docker Compose

### API Endpoints

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token

#### Properties
- `GET /api/properties/` - List properties (with filtering)
- `POST /api/properties/create/` - Create new property
- `GET /api/properties/{id}/` - Get property details
- `PUT /api/properties/{id}/update/` - Update property
- `DELETE /api/properties/{id}/delete/` - Delete property

#### Data Export
- `POST /api/exports/csv/` - Export properties to CSV
- `GET /api/exports/download/{id}/` - Download exported file

#### Bot Control
- `POST /api/bot/run/` - Run a specific scraper
- `POST /api/bot/run-all/` - Run all available scrapers
- `GET /api/bot/scrapers/` - List available scrapers

### Scraper System

The project includes a bot integration service that can:
- Run individual scrapers from the `real-estate-scraper-bot/scrapers/` directory
- Automatically map scraped data to Django models
- Upload scraped properties to the database
- Handle both `run_scraper()` function and `homesData` attribute patterns

### Command Line Tools

#### Standalone Scraper Runner
```bash
# List available scrapers
python run_scraper.py --list

# Run specific scraper
python run_scraper.py --scraper test_scraping1 --limit 5

# Run all scrapers
python run_scraper.py --all --limit 3

# Save results to file
python run_scraper.py --scraper test_scraping1 --output results.json
```

## Development

### Project Structure
```
django_real_estate_scraper/
├── real_estate_scraper/     # Django project settings
├── users/                   # User authentication app
├── properties/             # Property management app
├── exports/                # Data export app
├── services/               # Business logic services
│   └── bot_integration.py  # Scraper bot integration
├── run_scraper.py          # Standalone scraper runner
├── docker-compose.yml      # Docker services
├── Dockerfile             # Django container
└── requirements.txt        # Python dependencies
```

### Environment Variables
The bot integration service uses these environment variables:
- `BOT_API_URL` - Django API URL (default: http://127.0.0.1:8000/api)
- `BOT_USERNAME` - Bot username (default: testuser)
- `BOT_PASSWORD` - Bot password (default: testpass123)
- `BOT_RUNNING_FROM_DJANGO` - Whether running in Django context (default: true)
- `BOT_DIRECTORY` - Path to scraper bot directory

### Adding New Scrapers
1. Place scraper files in `real-estate-scraper-bot/scrapers/`
2. Ensure they either have a `run_scraper()` function or expose `homesData`
3. Use the bot API endpoints to run them

## Testing

### API Testing
1. Use the interactive documentation at `/api/docs/`
2. Test with curl commands (examples above)
3. Use tools like Postman or Insomnia

### Scraper Testing
1. Test individual scrapers: `python run_scraper.py --scraper test_scraping1`
2. Test via API: `POST /api/bot/run/` with `{"scraper_name": "test_scraping1"}`
3. Check database for uploaded properties




## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and development purposes.
