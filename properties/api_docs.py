"""
OpenAPI documentation schemas for Property endpoints
Separated from views for better organization and maintainability
"""

from drf_spectacular.utils import OpenApiParameter, OpenApiExample

# Property Create/Update Schema
PROPERTY_CREATE_SCHEMA = {
    'summary': "Create or Update Property",
    'description': "Create a new property or update existing one if reference number already exists. Photos field accepts a list of image URLs.",
    'tags': ["Properties"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'reference': {
                    'type': 'string',
                    'description': 'Unique reference number for the property',
                    'example': 'idealista_12345'
                },
                'title': {
                    'type': 'string',
                    'description': 'Property title/name',
                    'example': 'Beautiful apartment in Palma de Mallorca'
                },
                'category': {
                    'type': 'string',
                    'description': 'Property type (house, apartment, finca, etc.)',
                    'example': 'apartment'
                },
                'price': {
                    'type': 'number',
                    'description': 'Property price in euros',
                    'example': 450000.0
                },
                'square_meters': {
                    'type': 'number',
                    'description': 'Property size in square meters',
                    'example': 85.5
                },
                'region': {
                    'type': 'string',
                    'description': 'Property region/location',
                    'example': 'Mallorca'
                },
                'town': {
                    'type': 'string',
                    'description': 'Specific town/city',
                    'example': 'Palma de Mallorca'
                },
                'street_address': {
                    'type': 'string',
                    'description': 'Street address (optional)',
                    'example': 'Calle Mayor 123'
                },
                'address_city': {
                    'type': 'string',
                    'description': 'City name (optional)',
                    'example': 'Palma'
                },
                'address_state': {
                    'type': 'string',
                    'description': 'State/province (optional)',
                    'example': 'Islas Baleares'
                },
                'address_country': {
                    'type': 'string',
                    'description': 'Country name (optional)',
                    'example': 'Spain'
                },
                'bedrooms': {
                    'type': 'integer',
                    'description': 'Number of bedrooms',
                    'example': 3
                },
                'bathrooms': {
                    'type': 'integer',
                    'description': 'Number of bathrooms',
                    'example': 2
                },
                'land_area': {
                    'type': 'number',
                    'description': 'Land area in square meters (optional)',
                    'example': 120.0
                },
                'built_up': {
                    'type': 'number',
                    'description': 'Built area in square meters (optional)',
                    'example': 85.5
                },
                'description': {
                    'type': 'string',
                    'description': 'Property description (optional)',
                    'example': 'Luxurious apartment with sea views and modern amenities'
                },
                'photos': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'List of photo URLs (array of strings)',
                    'example': [
                        'https://example.com/photo1.jpg',
                        'https://example.com/photo2.jpg',
                        'https://example.com/photo3.jpg'
                    ]
                },
                'main_image': {
                    'type': 'string',
                    'description': 'Main/featured image URL (optional)',
                    'example': 'https://example.com/main-photo.jpg'
                },
                'features': {
                    'type': 'string',
                    'description': 'Property features (optional)',
                    'example': 'Sea view, Balcony, Air conditioning, Parking'
                },
                'platform': {
                    'type': 'string',
                    'description': 'Source platform name',
                    'example': 'idealista'
                },
                'link': {
                    'type': 'string',
                    'description': 'Original property listing URL',
                    'example': 'https://www.idealista.com/inmueble/12345/'
                },
                'energy_rating': {
                    'type': 'string',
                    'description': 'Energy efficiency rating (A-G)',
                    'enum': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'example': 'B'
                },
                'company_id': {
                    'type': 'string',
                    'description': 'Company/agency ID (optional)',
                    'example': 'comp_123'
                },
                'company_name': {
                    'type': 'string',
                    'description': 'Company/agency name (optional)',
                    'example': 'Real Estate Mallorca'
                },
                'property_created_at': {
                    'type': 'string',
                    'format': 'date-time',
                    'description': 'When property was created on platform (optional)',
                    'example': '2025-01-15T10:30:00Z'
                },
                'on_off': {
                    'type': 'boolean',
                    'description': 'Property availability status (optional)',
                    'example': True
                },
                'entity_id': {
                    'type': 'string',
                    'description': 'Entity identifier (optional)',
                    'example': 'ent_456'
                }
            },
            'required': ['reference', 'title', 'price', 'square_meters', 'region', 'platform', 'link']
        }
    },
    'responses': {
        200: {
            'description': 'Property updated successfully (if reference exists)',
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'reference': {'type': 'string'},
                'title': {'type': 'string'},
                'price': {'type': 'number'},
                'region': {'type': 'string'},
                'platform': {'type': 'string'},
                'created_at': {'type': 'string', 'format': 'date-time'},
                'updated_at': {'type': 'string', 'format': 'date-time'}
            }
        },
        201: {
            'description': 'Property created successfully',
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'reference': {'type': 'string'},
                'title': {'type': 'string'},
                'price': {'type': 'number'},
                'region': {'type': 'string'},
                'platform': {'type': 'string'},
                'created_at': {'type': 'string', 'format': 'date-time'},
                'updated_at': {'type': 'string', 'format': 'date-time'}
            }
        },
        400: {
            'description': 'Bad request - validation errors',
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        }
    },
    'examples': [
        OpenApiExample(
            'Create New Property',
            value={
                'reference': 'idealista_12345',
                'title': 'Beautiful apartment in Palma de Mallorca',
                'category': 'apartment',
                'price': 450000.0,
                'square_meters': 85.5,
                'region': 'Mallorca',
                'town': 'Palma de Mallorca',
                'bedrooms': 3,
                'bathrooms': 2,
                'description': 'Luxurious apartment with sea views and modern amenities',
                'photos': [
                    'https://example.com/photo1.jpg',
                    'https://example.com/photo2.jpg',
                    'https://example.com/photo3.jpg'
                ],
                'main_image': 'https://example.com/main-photo.jpg',
                'features': 'Sea view, Balcony, Air conditioning, Parking',
                'platform': 'idealista',
                'link': 'https://www.idealista.com/inmueble/12345/',
                'energy_rating': 'B'
            },
            request_only=True
        ),
        OpenApiExample(
            'Update Existing Property',
            value={
                'reference': 'idealista_12345',
                'price': 460000.0,
                'photos': [
                    'https://example.com/new-photo1.jpg',
                    'https://example.com/new-photo2.jpg'
                ]
            },
            request_only=True
        )
    ]
}

# Property List Schema
PROPERTY_LIST_SCHEMA = {
    'summary': "List Properties",
    'description': "Retrieve a list of properties with advanced filtering, search, and pagination capabilities.",
    'tags': ["Properties"],
    'parameters': [
        OpenApiParameter(
            name='search',
            type=str,
            description='Search in title, description, region, and town fields'
        ),
        OpenApiParameter(
            name='price_min',
            type=float,
            description='Minimum price filter (greater than or equal to)'
        ),
        OpenApiParameter(
            name='price_max',
            type=float,
            description='Maximum price filter (less than or equal to)'
        ),
        OpenApiParameter(
            name='square_meters_min',
            type=float,
            description='Minimum square meters filter (greater than or equal to)'
        ),
        OpenApiParameter(
            name='square_meters_max',
            type=float,
            description='Maximum square meters filter (less than or equal to)'
        ),
        OpenApiParameter(
            name='region',
            type=str,
            description='Filter by specific region (can be multiple, comma-separated)'
        ),
        OpenApiParameter(
            name='category',
            type=str,
            description='Filter by property category (can be multiple, comma-separated)'
        ),
        OpenApiParameter(
            name='bedrooms',
            type=int,
            description='Filter by minimum number of bedrooms (greater than or equal to)'
        ),
        OpenApiParameter(
            name='bathrooms',
            type=int,
            description='Filter by minimum number of bathrooms (greater than or equal to)'
        ),
        OpenApiParameter(
            name='land_area_min',
            type=float,
            description='Minimum land area filter (greater than or equal to)'
        ),
        OpenApiParameter(
            name='land_area_max',
            type=float,
            description='Maximum land area filter (less than or equal to)'
        ),
        OpenApiParameter(
            name='platform',
            type=str,
            description='Filter by source platform (exact match)'
        ),
        OpenApiParameter(
            name='energy_rating',
            type=str,
            description='Filter by energy rating (can be multiple, comma-separated)'
        ),
        OpenApiParameter(
            name='ordering',
            type=str,
            description='Sort by field (prefix with - for descending)'
        ),
        OpenApiParameter(
            name='page',
            type=int,
            description='Page number for pagination'
        ),
        OpenApiParameter(
            name='page_size',
            type=int,
            description='Number of properties per page (max 100)'
        )
    ],
    'responses': {
        200: {
            'description': 'List of properties with pagination',
            'type': 'object',
            'properties': {
                'count': {'type': 'integer', 'description': 'Total number of properties'},
                'next': {'type': 'string', 'description': 'URL for next page'},
                'previous': {'type': 'string', 'description': 'URL for previous page'},
                'results': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'reference': {'type': 'string'},
                            'title': {'type': 'string'},
                            'price': {'type': 'number'},
                            'square_meters': {'type': 'number'},
                            'region': {'type': 'string'},
                            'town': {'type': 'string'},
                            'bedrooms': {'type': 'integer'},
                            'bathrooms': {'type': 'integer'},
                            'platform': {'type': 'string'},
                            'created_at': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        }
    },
    'examples': [
        OpenApiExample(
            'Search for apartments in Palma',
            value={
                'search': 'palma apartment',
                'region': 'Mallorca',
                'category': 'apartment',
                'price_min': 300000,
                'price_max': 600000
            },
            request_only=True
        ),
        OpenApiExample(
            'Filter by bedrooms and price',
            value={
                'bedrooms': 2,
                'price_min': 400000,
                'ordering': '-price'
            },
            request_only=True
        ),
        OpenApiExample(
            'Filter by square meters and location',
            value={
                'square_meters_min': 80,
                'square_meters_max': 120,
                'region': 'Mallorca,Menorca',
                'category': 'house,apartment'
            },
            request_only=True
        )
    ]
}

# Bot Scrapers Schema
BOT_SCRAPERS_SCHEMA = {
    'summary': "Get Available Bot Scrapers",
    'description': "Retrieve a list of all available bot scrapers with their status and details.",
    'tags': ["Bot Control"],
    'responses': {
        200: {
            'description': 'List of available scrapers',
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'scrapers': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'status': {'type': 'string'},
                            'last_run': {'type': 'string', 'format': 'date-time'},
                            'properties_found': {'type': 'integer'}
                        }
                    }
                },
                'total_scrapers': {'type': 'integer'}
            }
        },
        500: {
            'description': 'Internal server error',
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'error': {'type': 'string'}
            }
        }
    }
}

# Run Bot Scraper Schema
RUN_BOT_SCRAPER_SCHEMA = {
    'summary': "Run Specific Bot Scraper",
    'description': "Execute a specific bot scraper to collect property data. The scraper will run immediately and return results.",
    'tags': ["Bot Control"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'scraper_name': {
                    'type': 'string',
                    'description': 'Name of the scraper to run',
                    'example': 'test_scraping1'
                },
                'upload_to_django': {
                    'type': 'boolean',
                    'description': 'Whether to upload scraped properties to Django',
                    'example': True
                },
                'limit_properties': {
                    'type': 'integer',
                    'description': 'Maximum number of properties to process',
                    'example': 3
                }
            },
            'required': ['scraper_name']
        }
    },
    'responses': {
        200: {
            'description': 'Scraper executed successfully',
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'message': {'type': 'string'},
                'scraper': {'type': 'string'},
                'uploaded_properties': {'type': 'integer'},
                'updated_properties': {'type': 'integer'},
                'total_processed': {'type': 'integer'}
            }
        },
        400: {
            'description': 'Bad request - invalid scraper name',
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'error': {'type': 'string'},
                'available_scrapers': {'type': 'array', 'items': {'type': 'string'}}
            }
        },
        500: {
            'description': 'Internal server error',
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'error': {'type': 'string'}
            }
        }
    },
    'examples': [
        OpenApiExample(
            'Run test_scraping1 with 3 properties',
            value={
                'scraper_name': 'test_scraping1',
                'upload_to_django': True,
                'limit_properties': 3
            },
            request_only=True
        ),
        OpenApiExample(
            'Success Response',
            value={
                'success': True,
                'message': 'Bot scraper test_scraping1 completed successfully',
                'scraper': 'test_scraping1',
                'uploaded_properties': 2,
                'updated_properties': 1,
                'total_processed': 3
            },
            response_only=True
        )
    ]
}

# Run All Scrapers Schema
RUN_ALL_SCRAPERS_SCHEMA = {
    'summary': "Run All Bot Scrapers",
    'description': "Execute all available bot scrapers simultaneously. Each scraper will run with the specified limits.",
    'tags': ["Bot Control"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'upload_to_django': {
                    'type': 'boolean',
                    'description': 'Whether to upload scraped properties to Django',
                    'example': True
                },
                'limit_properties': {
                    'type': 'integer',
                    'description': 'Maximum number of properties to process per scraper',
                    'example': 3
                }
            }
        }
    },
    'responses': {
        200: {
            'description': 'All scrapers executed successfully',
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'message': {'type': 'string'},
                'results': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'scraper': {'type': 'string'},
                            'uploaded': {'type': 'integer'},
                            'updated': {'type': 'integer'},
                            'success': {'type': 'boolean'},
                            'error': {'type': 'string'}
                        }
                    }
                },
                'total_scrapers': {'type': 'integer'}
            }
        },
        500: {
            'description': 'Internal server error',
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'error': {'type': 'string'}
            }
        }
    },
    'examples': [
        OpenApiExample(
            'Run all scrapers with 3 properties each',
            value={
                'upload_to_django': True,
                'limit_properties': 3
            },
            request_only=True
        ),
        OpenApiExample(
            'Success Response',
            value={
                'success': True,
                'message': 'All scrapers completed',
                'results': [
                    {
                        'scraper': 'test_scraping1',
                        'uploaded': 2,
                        'updated': 1,
                        'success': True
                    },
                    {
                        'scraper': 'test_scraping2',
                        'uploaded': 1,
                        'updated': 0,
                        'success': True
                    }
                ],
                'total_scrapers': 2
            },
            response_only=True
        )
    ]
}
