"""
OpenAPI documentation schemas for User Authentication endpoints
Separated from views for better organization and maintainability
"""

from drf_spectacular.utils import OpenApiExample

# User Login Schema
LOGIN_SCHEMA = {
    'summary': "User Login",
    'description': "Authenticate user and return JWT tokens",
    'tags': ["Authentication"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'description': "User's username", 'example': 'testuser'},
                'password': {'type': 'string', 'description': "User's password", 'example': 'testpass123'},
                'email': {'type': 'string', 'description': "User's email (optional)", 'example': 'test@example.com'},
            },
            'required': ['username', 'password']
        }
    },
    'responses': {
        200: {
            'description': 'Login successful',
            'type': 'object',
            'properties': {
                'access': {'type': 'string', 'description': 'JWT access token'},
                'refresh': {'type': 'string', 'description': 'JWT refresh token'},
                'user': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'username': {'type': 'string'},
                        'is_admin': {'type': 'boolean'},
                        'date_joined': {'type': 'string', 'format': 'date-time'},
                    }
                }
            }
        },
        400: {
            'description': 'Invalid credentials',
            'type': 'object',
            'properties': {
                'username': {'type': 'array', 'items': {'type': 'string'}},
                'password': {'type': 'array', 'items': {'type': 'string'}}
            }
        }
    },
    'examples': [
        OpenApiExample(
            'Successful Login',
            value={
                'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                'user': {
                    'id': 2,
                    'username': 'testuser',
                    'is_admin': True,
                    'date_joined': '2025-08-27T05:02:37.281192Z'
                }
            },
            response_only=True,
            status_codes=['200']
        )
    ]
}

# User Registration Schema
USER_CREATE_SCHEMA = {
    'summary': "User Registration",
    'description': "Create a new user account",
    'operationId': 'create_user',
    'tags': ["Authentication"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'description': 'Username for the new account', 'example': 'newuser'},
                'email': {'type': 'string', 'description': 'Email address', 'example': 'newuser@example.com'},
                'password': {'type': 'string', 'description': 'Password for the account', 'example': 'securepass123'},
                'password_confirm': {'type': 'string', 'description': 'Password confirmation', 'example': 'securepass123'},
            },
            'required': ['username', 'email', 'password', 'password_confirm']
        }
    },
    'responses': {
        201: {
            'description': 'User created successfully',
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'username': {'type': 'string'},
                'email': {'type': 'string'},
                'is_admin': {'type': 'boolean'},
                'date_joined': {'type': 'string', 'format': 'date-time'},
            }
        },
        400: {
            'description': 'Validation errors',
            'type': 'object',
            'properties': {
                'username': {'type': 'array', 'items': {'type': 'string'}},
                'email': {'type': 'array', 'items': {'type': 'string'}},
                'password': {'type': 'array', 'items': {'type': 'string'}},
                'password_confirm': {'type': 'array', 'items': {'type': 'string'}},
            }
        }
    },
    'examples': [
        OpenApiExample(
            'Successful Registration',
            value={
                'id': 3,
                'username': 'newuser',
                'email': 'newuser@example.com',
                'is_admin': False,
                'date_joined': '2025-08-27T05:02:37.281192Z'
            },
            response_only=True,
            status_codes=['201']
        )
    ]
}

# User Logout Schema
LOGOUT_SCHEMA = {
    'summary': "User Logout",
    'description': "Logout user and invalidate refresh token",
    'tags': ["Authentication"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh': {'type': 'string', 'description': 'Refresh token to invalidate', 'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'},
            },
            'required': ['refresh']
        }
    },
    'responses': {
        200: {
            'description': 'Logout successful',
            'type': 'object',
            'properties': {
                'message': {'type': 'string', 'example': 'Successfully logged out'}
            }
        },
        400: {
            'description': 'Invalid refresh token',
            'type': 'object',
            'properties': {
                'detail': {'type': 'string', 'example': 'Token is invalid or expired'}
            }
        }
    }
}

# Check Authentication Schema
CHECK_AUTH_SCHEMA = {
    'summary': "Check Authentication Status",
    'description': "Check if the current user is authenticated",
    'tags': ["Authentication"],
    'responses': {
        200: {
            'description': 'User is authenticated',
            'type': 'object',
            'properties': {
                'authenticated': {'type': 'boolean', 'example': True},
                'user': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'username': {'type': 'string'},
                        'is_admin': {'type': 'boolean'},
                    }
                }
            }
        },
        401: {
            'description': 'User is not authenticated',
            'type': 'object',
            'properties': {
                'authenticated': {'type': 'boolean', 'example': False},
                'detail': {'type': 'string', 'example': 'Authentication credentials were not provided'}
            }
        }
    }
}

# Check Admin Status Schema
CHECK_ADMIN_SCHEMA = {
    'summary': "Check Admin Status",
    'description': "Check if the current user has admin privileges",
    'tags': ["Authentication"],
    'responses': {
        200: {
            'description': 'User has admin privileges',
            'type': 'object',
            'properties': {
                'is_admin': {'type': 'boolean', 'example': True},
                'user': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'username': {'type': 'string'},
                        'is_admin': {'type': 'boolean'},
                    }
                }
            }
        },
        403: {
            'description': 'User does not have admin privileges',
            'type': 'object',
            'properties': {
                'is_admin': {'type': 'boolean', 'example': False},
                'detail': {'type': 'string', 'example': 'You do not have permission to perform this action'}
            }
        }
    }
}

# User List Schema (Admin Only)
USER_LIST_SCHEMA = {
    'summary': "List All Users",
    'description': "Get a list of all users (Admin only)",
    'tags': ["User Management"],
    'responses': {
        200: {
            'description': 'List of users',
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'is_admin': {'type': 'boolean'},
                    'date_joined': {'type': 'string', 'format': 'date-time'},
                }
            }
        },
        403: {
            'description': 'Access denied - admin privileges required',
            'type': 'object',
            'properties': {
                'detail': {'type': 'string', 'example': 'You do not have permission to perform this action'}
            }
        }
    }
}

# Add User Schema (Admin Only)
ADD_USER_SCHEMA = {
    'summary': "Add New User",
    'description': "Create a new user account (Admin only)",
    'tags': ["User Management"],
    'request': {
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'description': 'Username for the new account', 'example': 'newuser'},
                'email': {'type': 'string', 'description': 'Email address', 'example': 'newuser@example.com'},
                'password': {'type': 'string', 'description': 'Password for the account', 'example': 'securepass123'},
                'is_admin': {'type': 'boolean', 'description': 'Whether the user should have admin privileges', 'example': False},
            },
            'required': ['username', 'email', 'password']
        }
    },
    'responses': {
        201: {
            'description': 'User created successfully',
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'username': {'type': 'string'},
                'email': {'type': 'string'},
                'is_admin': {'type': 'boolean'},
                'date_joined': {'type': 'string', 'format': 'date-time'},
            }
        },
        400: {
            'description': 'Validation errors',
            'type': 'object',
            'properties': {
                'username': {'type': 'array', 'items': {'type': 'string'}},
                'email': {'type': 'array', 'items': {'type': 'string'}},
                'password': {'type': 'array', 'items': {'type': 'string'}},
            }
        },
        403: {
            'description': 'Access denied - admin privileges required',
            'type': 'object',
            'properties': {
                'detail': {'type': 'string', 'example': 'You do not have permission to perform this action'}
            }
        }
    }
}

# Delete User Schema (Admin Only)
DELETE_USER_SCHEMA = {
    'summary': "Delete User",
    'description': "Delete a user account (Admin only)",
    'tags': ["User Management"],
    'responses': {
        204: {
            'description': 'User deleted successfully'
        },
        403: {
            'description': 'Access denied - admin privileges required',
            'type': 'object',
            'properties': {
                'detail': {'type': 'string', 'example': 'You do not have permission to perform this action'}
            }
        },
        404: {
            'description': 'User not found',
            'type': 'object',
            'properties': {
                'detail': {'type': 'string', 'example': 'User not found'}
            }
        }
    }
}
