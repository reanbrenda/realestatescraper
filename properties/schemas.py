"""
OpenAPI schema definitions for Property endpoints
This keeps the views clean while maintaining full OpenAPI functionality
"""

# Property Create/Update Schema
PROPERTY_CREATE_SCHEMA = {
    'summary': "Create or Update Property",
    'description': "Create a new property or update existing one if reference number already exists. Photos field accepts a list of image URLs.",
    'tags': ["Properties"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'reference': {'type': 'string', 'description': 'Unique reference number', 'example': 'idealista_12345'},
                'title': {'type': 'string', 'description': 'Property title', 'example': 'Beautiful apartment in Palma'},
                'category': {'type': 'string', 'description': 'Property type', 'example': 'apartment'},
                'price': {'type': 'number', 'description': 'Price in euros', 'example': 450000.0},
                'square_meters': {'type': 'number', 'description': 'Size in m²', 'example': 85.5},
                'region': {'type': 'string', 'description': 'Property region', 'example': 'Mallorca'},
                'town': {'type': 'string', 'description': 'Specific town/city', 'example': 'Palma de Mallorca'},
                'bedrooms': {'type': 'integer', 'description': 'Number of bedrooms', 'example': 3},
                'bathrooms': {'type': 'integer', 'description': 'Number of bathrooms', 'example': 2},
                'description': {'type': 'string', 'description': 'Property description'},
                'photos': {
                    'type': 'array', 
                    'items': {'type': 'string'}, 
                    'description': 'List of photo URLs (array of strings)',
                    'example': ['https://example.com/photo1.jpg', 'https://example.com/photo2.jpg']
                },
                'platform': {'type': 'string', 'description': 'Source platform', 'example': 'idealista'},
                'link': {'type': 'string', 'description': 'Original listing URL', 'example': 'https://www.idealista.com/inmueble/12345/'}
            },
            'required': ['reference', 'title', 'price', 'square_meters', 'region', 'platform', 'link']
        }
    },
    'responses': {
        201: {'description': 'Property created successfully'},
        200: {'description': 'Property updated successfully'},
        400: {'description': 'Validation errors'}
    }
}

# Property List Schema
PROPERTY_LIST_SCHEMA = {
    'summary': "List Properties",
    'description': "List properties with filtering, search, and pagination",
    'tags': ["Properties"],
    'parameters': [
        {'name': 'search', 'in': 'query', 'description': 'Search in title, description, region, town', 'schema': {'type': 'string'}},
        {'name': 'price_min', 'in': 'query', 'description': 'Minimum price', 'schema': {'type': 'number'}},
        {'name': 'price_max', 'in': 'query', 'description': 'Maximum price', 'schema': {'type': 'number'}},
        {'name': 'bedrooms', 'in': 'query', 'description': 'Minimum bedrooms', 'schema': {'type': 'integer'}},
        {'name': 'region', 'in': 'query', 'description': 'Filter by region', 'schema': {'type': 'string'}},
        {'name': 'ordering', 'in': 'query', 'description': 'Sort by field (e.g., price, -price)', 'schema': {'type': 'string'}}
    ]
}

# Property Detail Schema
PROPERTY_DETAIL_SCHEMA = {
    'summary': "Get Property Details",
    'description': "Retrieve detailed information about a specific property by ID",
    'tags': ["Properties"]
}

# Property Update Schema
PROPERTY_UPDATE_SCHEMA = {
    'summary': "Update Property",
    'description': "Update an existing property with new data",
    'tags': ["Properties"]
}

# Property Delete Schema
PROPERTY_DELETE_SCHEMA = {
    'summary': "Delete Property",
    'description': "Delete a specific property by ID",
    'tags': ["Properties"]
}

# Property by Reference Schema
PROPERTY_BY_REFERENCE_SCHEMA = {
    'summary': "Get Property by Reference",
    'description': "Retrieve a property by its unique reference number",
    'tags': ["Properties"]
}

# All Regions Schema
ALL_REGIONS_SCHEMA = {
    'summary': "Get All Regions",
    'description': "Retrieve a list of all unique regions where properties are located",
    'tags': ["Properties"]
}

# Patch Property Schema
PATCH_PROPERTY_SCHEMA = {
    'summary': "Patch Property",
    'description': "Partially update a property with PATCH method",
    'tags': ["Properties"]
}

# Bot Scrapers Schema
BOT_SCRAPERS_SCHEMA = {
    'summary': "Get Available Bot Scrapers",
    'description': "Retrieve a list of all available bot scrapers with their status and details (Admin only)",
    'tags': ["Bot Control"]
}

# Run Bot Scraper Schema
RUN_BOT_SCRAPER_SCHEMA = {
    'summary': "Run Specific Bot Scraper",
    'description': "Execute a specific bot scraper to collect property data (Admin only)",
    'tags': ["Bot Control"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'scraper_name': {'type': 'string', 'description': 'Name of the scraper to run', 'example': 'test_scraping1'},
                'upload_to_django': {'type': 'boolean', 'description': 'Whether to upload scraped properties to Django', 'example': True},
                'limit_properties': {'type': 'integer', 'description': 'Maximum number of properties to process', 'example': 3}
            },
            'required': ['scraper_name']
        }
    }
}

# Run All Scrapers Schema
RUN_ALL_SCRAPERS_SCHEMA = {
    'summary': "Run All Bot Scrapers",
    'description': "Execute all available bot scrapers simultaneously (Admin only)",
    'tags': ["Bot Control"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'upload_to_django': {'type': 'boolean', 'description': 'Whether to upload scraped properties to Django', 'example': True},
                'limit_properties': {'type': 'integer', 'description': 'Maximum number of properties to process per scraper', 'example': 3}
            }
        }
    }
}
