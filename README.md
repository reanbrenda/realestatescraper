# Real Estate Scraper API

A Django-based API for real estate property scraping, management, and data export.

## Features

- Property Management: Full CRUD operations for real estate properties
- Web Scraping Integration: Automated property data collection from multiple platforms
- Advanced Filtering: Comprehensive search and filter capabilities
- Data Export: Multiple export formats (CSV, PDF, JSON)
- User Authentication: JWT-based authentication with admin controls
- API Documentation: Complete OpenAPI/Swagger documentation
- Docker Support: Containerized deployment with Docker Compose

## Architecture

```
django_real_estate_scraper/
├── real_estate_scraper/          # Django project settings
├── properties/                   # Property management app
├── users/                        # User authentication app
├── exports/                      # Data export functionality
├── services/                     # Business logic services
├── utils/                        # Utility functions
├── real-estate-scraper-bot/      # Web scraping bot
└── static/                       # Static files
```

## Technology Stack

- Backend: Django 5.0 + Django REST Framework
- Database: PostgreSQL
- Authentication: JWT (djangorestframework-simplejwt)
- API Documentation: drf-spectacular
- Filtering: django-filter
- Export: reportlab (PDF), csv, json
- Containerization: Docker + Docker Compose

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL (handled by Docker)

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd django_real_estate_scraper
cp env.example .env
# Edit .env with your configuration
```

### 2. Start Services

```bash
docker compose up -d
```

### 3. Run Migrations

```bash
docker compose exec django python manage.py migrate
```

### 4. Create Superuser

```bash
docker compose exec django python manage.py createsuperuser
```

### 5. Access the Application

- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Documentation: http://localhost:8000/api/docs/

## API Authentication

### Get Access Token

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Use Token

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/properties/
```

## API Endpoints

### Properties
- `GET /api/properties/` - List properties with filtering
- `POST /api/properties/create/` - Create/update property
- `GET /api/properties/{id}/` - Get property details
- `PATCH /api/properties/{id}/` - Update property
- `DELETE /api/properties/{id}/` - Delete property

### Bot Control (Admin Only)
- `GET /api/bot/scrapers/` - List available scrapers
- `POST /api/bot/run/` - Run specific scraper
- `POST /api/bot/run-all/` - Run all scrapers

### Data Export
- `POST /api/export/csv/` - Export to CSV
- `POST /api/export/pdf/` - Export to PDF
- `POST /api/export/json/` - Export to JSON

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration

## Filtering Examples

### Search Properties
```bash
# Search for apartments in Palma
curl "http://localhost:8000/api/properties/?search=palma%20apartment&region=Mallorca"

# Filter by price and bedrooms
curl "http://localhost:8000/api/properties/?price_min=300000&price_max=600000&bedrooms=2"

# Sort by price (highest first)
curl "http://localhost:8000/api/properties/?ordering=-price"
```

## Bot Scraping

### Run Specific Scraper
```bash
curl -X POST http://localhost:8000/api/bot/run/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"scraper_name": "test_scraping1", "limit_properties": 3}'
```

### Run All Scrapers
```bash
curl -X POST http://localhost:8000/api/bot/run-all/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit_properties": 3}'
```

## Project Structure

```
properties/           # Property management
├── models.py        # Property data models
├── views.py         # API views and endpoints
├── serializers.py   # Data serialization
├── filters.py       # Advanced filtering
├── api_docs.py      # OpenAPI documentation
└── urls.py          # URL routing

users/               # User management
├── models.py        # Custom user model
├── views.py         # Authentication views
├── serializers.py   # User serializers
└── permissions.py   # Custom permissions

exports/             # Data export
├── views.py         # Export endpoints
├── api_docs.py      # Export documentation
└── urls.py          # Export routing

services/            # Business logic
└── bot_integration.py  # Bot integration service

utils/               # Utilities
├── hash.py          # Password hashing
├── jwt.py           # JWT utilities
└── vector_search.py # Vector search functionality
```

## Configuration

### Environment Variables

```bash
# Database
DB_HOST=db
DB_NAME=real_estate
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key
DEBUG=1
DJANGO_SETTINGS_MODULE=real_estate_scraper.settings

# JWT
JWT_SECRET=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# Bot Integration
BOT_API_URL=http://django:8000/api
BOT_USERNAME=your_bot_username
BOT_PASSWORD=your_bot_password
```

## Testing

### Run Tests
```bash
docker compose exec django python manage.py test
```

### Test API Endpoints
```bash
# Test property creation
curl -X POST http://localhost:8000/api/properties/create/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reference": "test_123",
    "title": "Test Property",
    "price": 300000,
    "square_meters": 80,
    "region": "Test Region",
    "platform": "test",
    "link": "https://example.com"
  }'
```

## Deployment

### Production Settings

1. Update `.env` with production values
2. Set `DEBUG=0`
3. Configure production database
4. Set secure `SECRET_KEY`
5. Configure static file serving
6. Set up reverse proxy (nginx)

### Docker Production

```bash
# Build production image
docker build -t real-estate-scraper:prod .

# Run with production compose
docker compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/api/docs/`
- Review the troubleshooting guide

## Changelog

### v1.0.0
- Initial release
- Property management API
- Bot scraping integration
- Data export functionality
- JWT authentication
- OpenAPI documentation

---

Built with Django and modern web technologies
