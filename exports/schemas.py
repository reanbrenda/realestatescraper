"""
OpenAPI schema definitions for Export endpoints
This keeps the views clean while maintaining full OpenAPI functionality
"""

# CSV Export Schema
EXPORT_CSV_SCHEMA = {
    'summary': "Export Properties to CSV",
    'description': "Export properties to CSV format with property data",
    'tags': ["Data Export"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'property_ids': {
                    'type': 'array',
                    'description': 'Array of property IDs to export',
                    'items': {'type': 'integer'},
                    'example': [1, 2, 3],
                    'minItems': 1
                }
            },
            'required': ['property_ids']
        }
    },
    'responses': {
        200: {
            'description': 'CSV export successful',
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
            'description': 'Invalid export parameters',
            'type': 'object',
            'properties': {
                'error': {'type': 'string', 'example': 'property_ids is required'}
            }
        }
    }
}

# PDF Export Schema
EXPORT_PDF_SCHEMA = {
    'summary': "Export Properties to PDF",
    'description': "Export properties to PDF format with professional table layout (max 4 properties for optimal layout)",
    'tags': ["Data Export"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'property_ids': {
                    'type': 'array',
                    'description': 'Array of property IDs to export (max 4 for optimal layout)',
                    'items': {'type': 'integer'},
                    'example': [1, 2, 3, 4],
                    'minItems': 1,
                    'maxItems': 4
                }
            },
            'required': ['property_ids']
        }
    },
    'responses': {
        200: {
            'description': 'PDF export successful',
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
            'description': 'Invalid export parameters',
            'type': 'object',
            'properties': {
                'error': {'type': 'string', 'example': 'property_ids is required'}
            }
        }
    }
}

# JSON Export Schema
EXPORT_JSON_SCHEMA = {
    'summary': "Export Properties to JSON",
    'description': "Export properties to JSON format with complete property data",
    'tags': ["Data Export"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'property_ids': {
                    'type': 'array',
                    'description': 'Array of property IDs to export',
                    'items': {'type': 'integer'},
                    'example': [1, 2, 3],
                    'minItems': 1
                }
            },
            'required': ['property_ids']
        }
    },
    'responses': {
        200: {
            'description': 'JSON export successful',
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
            'description': 'Invalid export parameters',
            'type': 'object',
            'properties': {
                'error': {'type': 'string', 'example': 'property_ids is required'}
            }
        }
    }
}
