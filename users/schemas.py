"""
OpenAPI schema definitions for User endpoints
This keeps the views clean while maintaining full OpenAPI functionality
"""

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
    }
}

# User Registration Schema
USER_CREATE_SCHEMA = {
    'summary': "User Registration",
    'description': "Create a new user account",
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
    }
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
                'refresh_token': {'type': 'string', 'description': 'Refresh token to invalidate', 'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'},
            },
            'required': ['refresh_token']
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
                'error': {'type': 'string', 'example': 'Refresh token is required'}
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
                'user_id': {'type': 'integer', 'example': 1}
            }
        },
        401: {
            'description': 'User is not authenticated',
            'type': 'object',
            'properties': {
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
            'description': 'User admin status',
            'type': 'object',
            'properties': {
                'is_admin': {'type': 'boolean', 'example': True},
                'user_id': {'type': 'integer', 'example': 1}
            }
        },
        401: {
            'description': 'User is not authenticated',
            'type': 'object',
            'properties': {
                'detail': {'type': 'string', 'example': 'Authentication credentials were not provided'}
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
        200: {
            'description': 'User deleted successfully',
            'type': 'object',
            'properties': {
                'message': {'type': 'string', 'example': 'User deleted successfully'}
            }
        },
        400: {
            'description': 'Cannot delete yourself',
            'type': 'object',
            'properties': {
                'error': {'type': 'string', 'example': 'Cannot delete yourself'}
            }
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
                'error': {'type': 'string', 'example': 'User not found'}
            }
        }
    }
}
