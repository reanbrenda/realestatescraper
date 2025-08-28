# Project Structure Documentation

This document provides a detailed overview of the Real Estate Scraper API project structure, explaining the purpose and organization of each component.

## 📁 Root Directory Structure

```
django_real_estate_scraper/
├── README.md                    # Project overview and setup instructions
├── PROJECT_STRUCTURE.md         # This file - detailed structure documentation
├── API_COVERAGE.md             # API endpoint documentation and coverage
├── requirements.txt             # Python dependencies with version pinning
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Multi-service container orchestration
├── env.example                 # Environment variables template
├── manage.py                   # Django management script
├── .gitignore                  # Git ignore patterns
│
├── real_estate_scraper/        # Main Django project package
├── properties/                 # Property management application
├── users/                      # User authentication application
├── exports/                    # Data export functionality
├── services/                   # Business logic services
├── utils/                      # Utility functions and helpers
├── real-estate-scraper-bot/    # Web scraping bot integration
├── static/                     # Static files (CSS, JS, images)
├── media/                      # User-uploaded files
└── staticfiles/                # Collected static files
```

## 🏗️ Django Project Structure

### `real_estate_scraper/` - Main Project Package

This is the core Django project configuration package containing:

- **`__init__.py`**: Python package initialization
- **`settings.py`**: Django project settings and configuration
- **`urls.py`**: Main URL routing configuration
- **`wsgi.py`**: WSGI application entry point
- **`asgi.py`**: ASGI application entry point
- **`admin.py`**: Global admin site configuration

**Key Responsibilities:**
- Project-level configuration management
- URL routing and middleware configuration
- Database and authentication settings
- Static and media file configuration
- Third-party app integration

## 🏠 Applications Structure

### `properties/` - Property Management Application

**Purpose**: Core application for managing real estate properties

**Components**:
- **`models.py`**: Property data models and database schema
- **`views.py`**: API views and business logic
- **`serializers.py`**: Data serialization for API responses
- **`filters.py`**: Advanced filtering and search functionality
- **`api_docs.py`**: OpenAPI documentation schemas
- **`urls.py`**: Property-specific URL routing
- **`admin.py`**: Django admin interface configuration
- **`pagination.py`**: Custom pagination classes

**Key Features**:
- CRUD operations for properties
- Advanced filtering and search
- Pagination and sorting
- Reference-based property updates
- Comprehensive API documentation

### `users/` - User Authentication Application

**Purpose**: User management and authentication system

**Components**:
- **`models.py`**: Custom user model with admin privileges
- **`views.py`**: Authentication views (login, register)
- **`serializers.py`**: User data serialization
- **`permissions.py`**: Custom permission classes
- **`urls.py`**: Authentication URL routing
- **`admin.py`**: User admin interface

**Key Features**:
- JWT-based authentication
- Custom user model with admin roles
- Secure password handling
- Permission-based access control

### `exports/` - Data Export Application

**Purpose**: Export property data in various formats

**Components**:
- **`views.py`**: Export endpoint views
- **`api_docs.py`**: Export API documentation
- **`urls.py`**: Export URL routing

**Key Features**:
- CSV export with custom formatting
- PDF export with professional layout
- JSON export with full property details
- Bulk export capabilities

## 🔧 Services and Utilities

### `services/` - Business Logic Services

**Purpose**: Centralized business logic and external integrations

**Components**:
- **`bot_integration.py`**: Web scraping bot integration service

**Key Features**:
- Bot scraper management
- Property data processing
- API integration with external scrapers
- Error handling and logging

### `utils/` - Utility Functions

**Purpose**: Reusable utility functions and helpers

**Components**:
- **`hash.py`**: Password hashing utilities
- **`jwt.py`**: JWT token utilities
- **`vector_search.py`**: Vector search functionality

**Key Features**:
- Security utilities
- Token management
- AI-powered search capabilities

## 🤖 Bot Integration

### `real-estate-scraper-bot/` - Web Scraping Bot

**Purpose**: External web scraping bot for property data collection

**Components**:
- **`scrapers/`**: Individual scraper modules
- **`upload.py`**: Data upload and transformation
- **`main.py`**: Bot entry point
- **`requirements.txt`**: Bot-specific dependencies

**Key Features**:
- Multiple scraper implementations
- Data transformation and cleaning
- API integration for data upload
- Error handling and retry logic

## 📁 Static and Media Files

### `static/` - Static Files
- CSS stylesheets
- JavaScript files
- Images and icons
- Font files

### `media/` - User Uploads
- Property images
- Document uploads
- Temporary files

### `staticfiles/` - Collected Static Files
- Production-ready static files
- Generated by `collectstatic` command

## 🐳 Docker Configuration

### `Dockerfile`
- Multi-stage build optimization
- Security best practices
- Health checks
- Non-root user execution

### `docker-compose.yml`
- Service orchestration
- Volume management
- Network configuration
- Health checks and dependencies

## 🔐 Configuration Management

### Environment Variables
- **Development**: `.env` file (not in version control)
- **Template**: `env.example` with comprehensive examples
- **Production**: Environment-specific configuration

### Key Configuration Areas
- Database settings
- JWT authentication
- CORS configuration
- Bot integration
- AI services
- Logging and monitoring

## 📚 Documentation Structure

### API Documentation
- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`
- **OpenAPI Schema**: `/api/schema/`

### Code Documentation
- **Docstrings**: Comprehensive function and class documentation
- **Type Hints**: Python type annotations
- **Comments**: Inline code explanations

## 🧪 Testing and Quality

### Testing Structure
- Unit tests for models and views
- Integration tests for API endpoints
- Test data and fixtures
- Coverage reporting

### Code Quality
- **Linting**: flake8, black, isort
- **Type Checking**: mypy
- **Security**: bandit, safety
- **Documentation**: pydocstyle

## 🚀 Deployment and Operations

### Development
- Local development server
- Docker Compose for services
- Hot reloading
- Debug tools

### Production
- Gunicorn WSGI server
- Nginx reverse proxy
- PostgreSQL database
- Redis caching (optional)
- Monitoring and logging

## 📊 Monitoring and Logging

### Logging Configuration
- Structured logging
- Log levels and rotation
- Error tracking
- Performance monitoring

### Health Checks
- Application health endpoints
- Database connectivity
- External service status
- Docker health checks

## 🔒 Security Considerations

### Authentication
- JWT token management
- Password security
- Rate limiting
- CORS configuration

### Data Protection
- Input validation
- SQL injection prevention
- XSS protection
- CSRF protection

---

This structure provides a scalable, maintainable foundation for the Real Estate Scraper API, following Django best practices and modern development standards.
