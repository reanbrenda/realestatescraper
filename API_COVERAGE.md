# API Coverage Documentation

This document provides comprehensive coverage of all API endpoints in the Real Estate Scraper API, including request/response formats, authentication requirements, and usage examples.

## Authentication

All API endpoints (except login/register) require JWT authentication via the `Authorization` header:

```bash
Authorization: Bearer <your-jwt-token>
```

### JWT Token Lifetime
- Access Token: 24 hours
- Refresh Token: 7 days

## Property Management API

### 1. Property CRUD Operations

#### Create/Update Property
- **Endpoint**: `POST /api/properties/create/`
- **Description**: Create a new property or update existing one if reference exists
- **Authentication**: Required
- **Features**:
  - Auto-update if reference number exists
  - Photos field accepts array of image URLs
  - Flexible data validation
  - Reference-based deduplication

**Request Body**:
```json
{
  "reference": "idealista_12345",
  "title": "Beautiful apartment in Palma",
  "price": 450000.0,
  "square_meters": 85.5,
  "region": "Mallorca",
  "platform": "idealista",
  "link": "https://www.idealista.com/inmueble/12345/",
  "photos": [
    "https://example.com/photo1.jpg",
    "https://example.com/photo2.jpg"
  ]
}
```

**Response**:
- `201 Created`: New property created
- `200 OK`: Existing property updated
- `400 Bad Request`: Validation errors

#### List Properties
- **Endpoint**: `GET /api/properties/`
- **Description**: Retrieve properties with advanced filtering and pagination
- **Authentication**: Required
- **Features**:
  - Advanced search and filtering
  - Pagination (100 properties per page)
  - Sorting and ordering
  - Multiple filter combinations

**Query Parameters**:
- `search`: Text search in title, description, region, town
- `price_min`/`price_max`: Price range filtering
- `square_meters_min`/`square_meters_max`: Size range filtering
- `bedrooms`: Minimum bedrooms (≥)
- `bathrooms`: Minimum bathrooms (≥)
- `region`: Filter by region (supports multiple, comma-separated)
- `category`: Filter by property type (supports multiple)
- `platform`: Filter by source platform
- `energy_rating`: Filter by energy rating (supports multiple)
- `ordering`: Sort by field (`price`, `-price`, `square_meters`, etc.)
- `page`: Page number for pagination
- `page_size`: Items per page (max 100)

**Example Usage**:
```bash
# Search for apartments in Palma
curl "http://localhost:8000/api/properties/?search=palma%20apartment&region=Mallorca&category=apartment"

# Filter by price and bedrooms
curl "http://localhost:8000/api/properties/?price_min=300000&price_max=600000&bedrooms=2"

# Sort by price (highest first)
curl "http://localhost:8000/api/properties/?ordering=-price"
```

#### Get Property Details
- **Endpoint**: `GET /api/properties/{id}/`
- **Description**: Retrieve specific property by ID
- **Authentication**: Required

#### Update Property
- **Endpoint**: `PUT /api/properties/{id}/update/`
- **Description**: Update specific property
- **Authentication**: Required

#### Delete Property
- **Endpoint**: `DELETE /api/properties/{id}/delete/`
- **Description**: Delete specific property
- **Authentication**: Required

#### Patch Property
- **Endpoint**: `PATCH /api/properties/{id}/`
- **Description**: Partial update of property
- **Authentication**: Required
- **Features**: Flexible partial updates

#### Get Property by Reference
- **Endpoint**: `GET /api/properties/reference/{reference}/`
- **Description**: Retrieve property by reference number
- **Authentication**: Required

#### Get All Regions
- **Endpoint**: `GET /api/properties/regions/`
- **Description**: Get list of all unique regions
- **Authentication**: Required

## Bot Control API (Admin Only)

### 1. Bot Scraper Management

#### List Available Scrapers
- **Endpoint**: `GET /api/bot/scrapers/`
- **Description**: Get list of all available bot scrapers with status
- **Authentication**: Required (Admin only)
- **Response**: List of scrapers with details and status

#### Run Specific Scraper
- **Endpoint**: `POST /api/bot/run/`
- **Description**: Execute a specific bot scraper
- **Authentication**: Required (Admin only)
- **Features**:
  - Configurable property limits
  - Upload to Django option
  - Real-time execution
  - Detailed results

**Request Body**:
```json
{
  "scraper_name": "test_scraping1",
  "upload_to_django": true,
  "limit_properties": 3
}
```

**Response**:
```json
{
  "success": true,
  "message": "Bot scraper test_scraping1 completed successfully",
  "scraper": "test_scraping1",
  "uploaded_properties": 2,
  "updated_properties": 1,
  "total_processed": 3
}
```

#### Run All Scrapers
- **Endpoint**: `POST /api/bot/run-all/`
- **Description**: Execute all available scrapers simultaneously
- **Authentication**: Required (Admin only)
- **Features**:
  - Parallel execution
  - Individual scraper results
  - Configurable limits per scraper

**Request Body**:
```json
{
  "upload_to_django": true,
  "limit_properties": 3
}
```

**Response**:
```json
{
  "success": true,
  "message": "All scrapers completed",
  "results": [
    {
      "scraper": "test_scraping1",
      "uploaded": 2,
      "updated": 1,
      "success": true
    }
  ],
  "total_scrapers": 1
}
```

## Data Export API

### 1. Export Formats

#### Export to CSV
- **Endpoint**: `POST /api/export/csv/`
- **Description**: Export selected properties to CSV format
- **Authentication**: Required
- **Features**:
  - Custom CSV formatting
  - All property fields included
  - Downloadable file response

**Request Body**:
```json
{
  "property_ids": [1, 2, 3, 4, 5]
}
```

#### Export to PDF
- **Endpoint**: `POST /api/export/pdf/`
- **Description**: Export selected properties to PDF format
- **Authentication**: Required
- **Features**:
  - Professional PDF layout
  - Limited to 4 properties for optimal layout
  - Downloadable file response

**Request Body**:
```json
{
  "property_ids": [1, 2, 3, 4]
}
```

#### Export to JSON
- **Endpoint**: `POST /api/export/json/`
- **Description**: Export selected properties to JSON format
- **Authentication**: Required
- **Features**:
  - Full property details
  - Structured JSON response
  - Downloadable file response

**Request Body**:
```json
{
  "property_ids": [1, 2, 3, 4, 5]
}
```

## User Authentication API

### 1. Authentication Endpoints

#### User Login
- **Endpoint**: `POST /api/auth/login/`
- **Description**: Authenticate user and return JWT tokens
- **Authentication**: Not required
- **Features**:
  - Username/password authentication
  - JWT token generation
  - User information response

**Request Body**:
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

**Response**:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 2,
    "username": "testuser",
    "is_admin": true,
    "date_joined": "2025-08-27T05:02:37.281192Z"
  }
}
```

#### User Registration
- **Endpoint**: `POST /api/auth/register/`
- **Description**: Create new user account
- **Authentication**: Not required
- **Features**:
  - User account creation
  - Password validation
  - Admin approval system

## Advanced Features

### 1. Search and Filtering

**Text Search**:
- Searches across multiple fields: title, description, region, town
- Case-insensitive matching
- Partial word matching

**Range Filters**:
- Price ranges with min/max values
- Square meter ranges
- Land area ranges
- All ranges support greater than/less than operations

**Multiple Choice Filters**:
- Region selection (supports multiple regions)
- Category selection (supports multiple categories)
- Energy rating selection (supports multiple ratings)

**Exact Match Filters**:
- Platform filtering
- Specific field matching

### 2. Pagination and Sorting

**Pagination**:
- Default page size: 100 properties
- Configurable page size (max 100)
- Page navigation with next/previous links
- Total count information

**Sorting**:
- Default: Creation date (newest first)
- Custom sorting by any field
- Descending order with `-` prefix
- Supported fields: price, square_meters, created_at, updated_at

### 3. Data Validation

**Required Fields**:
- reference: Unique property identifier
- title: Property title/name
- price: Property price
- square_meters: Property size
- region: Property location
- platform: Source platform
- link: Original listing URL

**Optional Fields**:
- category: Property type
- town: Specific town/city
- bedrooms: Number of bedrooms
- bathrooms: Number of bathrooms
- description: Property description
- photos: Array of image URLs
- energy_rating: Energy efficiency rating
- And many more...

## Response Formats

### 1. Success Responses

**Standard Success**:
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {...}
}
```

**List Responses**:
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/properties/?page=2",
  "previous": null,
  "results": [...]
}
```

### 2. Error Responses

**Validation Errors**:
```json
{
  "field_name": ["This field is required."],
  "price": ["A valid number is required."]
}
```

**Authentication Errors**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Permission Errors**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

## Performance Considerations

### 1. Database Optimization
- Indexed fields for common queries
- Efficient filtering with django-filter
- Pagination to limit result sets
- Optimized database queries

### 2. Caching Strategy
- Static file caching
- Database query optimization
- Response caching for read operations

### 3. Rate Limiting
- Authentication-based rate limiting
- API endpoint throttling
- Bot protection mechanisms

## Security Features

### 1. Authentication & Authorization
- JWT-based authentication
- Role-based access control
- Admin-only endpoints protection
- Secure password handling

### 2. Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection

### 3. API Security
- CORS configuration
- Request size limits
- File upload restrictions
- Secure headers

## API Documentation

### 1. Interactive Documentation
- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`
- **OpenAPI Schema**: `/api/schema/`

### 2. Code Examples
- cURL examples for all endpoints
- Python client examples
- JavaScript client examples
- Postman collection

### 3. Testing Tools
- Built-in Django test framework
- API endpoint testing
- Integration testing
- Performance testing

---

This API provides comprehensive coverage for real estate property management, web scraping integration, and data export functionality, with professional-grade security, performance, and documentation features.
