"""
OpenAPI documentation schemas for Export endpoints
Separated from views for better organization and maintainability
"""

from drf_spectacular.utils import OpenApiExample

# Export CSV Schema
EXPORT_CSV_SCHEMA = {
    'summary': "Export Properties to CSV",
    'description': "Export selected properties to CSV format. Send a list of property IDs to export specific properties.",
    'tags': ["Data Export"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'property_ids': {
                    'type': 'array',
                    'items': {'type': 'integer'},
                    'description': 'List of property IDs to export',
                    'example': [1, 2, 3, 4, 5]
                }
            },
            'required': ['property_ids']
        }
    },
    'responses': {
        200: {
            'description': 'CSV file download',
            'content': {
                'text/csv': {
                    'schema': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        400: {
            'description': 'Bad request - missing property_ids',
            'type': 'object',
            'properties': {
                'error': {'type': 'string', 'example': 'property_ids is required'}
            }
        }
    },
    'examples': [
        OpenApiExample(
            'Export 3 Properties',
            value={'property_ids': [1, 2, 3]},
            request_only=True
        )
    ]
}

# Export PDF Schema
EXPORT_PDF_SCHEMA = {
    'summary': "Export Properties to PDF",
    'description': "Export selected properties to PDF format. Limited to 4 properties for optimal PDF layout.",
    'tags': ["Data Export"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'property_ids': {
                    'type': 'array',
                    'items': {'type': 'integer'},
                    'description': 'List of property IDs to export (max 4 for PDF)',
                    'example': [1, 2, 3, 4]
                }
            },
            'required': ['property_ids']
        }
    },
    'responses': {
        200: {
            'description': 'PDF file download',
            'content': {
                'application/pdf': {
                    'schema': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        400: {
            'description': 'Bad request - missing property_ids',
            'type': 'object',
            'properties': {
                'error': {'type': 'string', 'example': 'property_ids is required'}
            }
        }
    },
    'examples': [
        OpenApiExample(
            'Export 4 Properties to PDF',
            value={'property_ids': [1, 2, 3, 4]},
            request_only=True
        )
    ]
}

# Export JSON Schema
EXPORT_JSON_SCHEMA = {
    'summary': "Export Properties to JSON",
    'description': "Export selected properties to JSON format with full property details.",
    'tags': ["Data Export"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'property_ids': {
                    'type': 'array',
                    'items': {'type': 'integer'},
                    'description': 'List of property IDs to export',
                    'example': [1, 2, 3, 4, 5]
                }
            },
            'required': ['property_ids']
        }
    },
    'responses': {
        200: {
            'description': 'JSON file download with property data',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'reference': {'type': 'string'},
                                'title': {'type': 'string'},
                                'category': {'type': 'string'},
                                'price': {'type': 'number'},
                                'square_meters': {'type': 'number'},
                                'region': {'type': 'string'},
                                'town': {'type': 'string'},
                                'bedrooms': {'type': 'integer'},
                                'bathrooms': {'type': 'integer'},
                                'platform': {'type': 'string'},
                                'link': {'type': 'string'},
                                'created_at': {'type': 'string', 'format': 'date-time'}
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad request - missing property_ids',
            'type': 'object',
            'properties': {
                'error': {'type': 'string', 'example': 'property_ids is required'}
            }
        }
    },
    'examples': [
        OpenApiExample(
            'Export 3 Properties to JSON',
            value={'property_ids': [1, 2, 3]},
            request_only=True
        ),
        OpenApiExample(
            'JSON Response Example',
            value=[
                {
                    'reference': 'idealista_123',
                    'title': 'Beautiful apartment in Palma',
                    'price': 450000,
                    'region': 'Mallorca',
                    'platform': 'idealista'
                }
            ],
            response_only=True
        )
    ]
}
