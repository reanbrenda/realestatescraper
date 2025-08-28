from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer
from .permissions import IsAdminUser
# OpenAPI documentation schemas defined directly in decorators

User = get_user_model()


@extend_schema(
    summary="User Registration",
    description="Create a new user account",
    tags=["Authentication"],
    request={
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
    responses={
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
)
class UserCreateView(generics.CreateAPIView):
    """View for creating new users"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    summary="List All Users",
    description="Get a list of all users (Admin only)",
    tags=["User Management"]
)
class UserListView(generics.ListAPIView):
    """View for listing users (admin only)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    summary="User Detail",
    description="Retrieve, update, and delete users",
    tags=["User Management"]
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    summary="User Login",
    description="Authenticate user and return JWT tokens",
    tags=["Authentication"],
    request={
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
    responses={
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
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    User login endpoint
    
    Authenticates a user with username and password, returning JWT access and refresh tokens.
    The access token is valid for 24 hours and should be included in subsequent API requests.
    
    **Request Body:**
    - username (required): User's username
    - password (required): User's password  
    - email (optional): User's email address
    
    **Response:**
    - access: JWT access token for API authentication
    - refresh: JWT refresh token for getting new access tokens
    - user: User object with basic information
    
    **Example Usage:**
    ```bash
    curl -X POST http://localhost:8000/api/auth/login/ \\
      -H "Content-Type: application/json" \\
      -d '{"username": "testuser", "password": "testpass123"}'
    ```
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="User Logout",
    description="Logout user and invalidate refresh token",
    tags=["Authentication"]
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'})
        else:
            return Response({'error': 'Refresh token is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Invalid token'}, 
                       status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Check Authentication Status",
    description="Check if the current user is authenticated",
    tags=["Authentication"]
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_auth(request):
    """Check if user is authenticated and return user_id"""
    return Response({'user_id': request.user.id})


@extend_schema(
    summary="Check Admin Status",
    description="Check if the current user has admin privileges",
    tags=["Authentication"]
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_admin(request):
    """Check if user has admin privileges"""
    if hasattr(request.user, 'is_admin') and request.user.is_admin:
        return Response({'is_admin': True, 'user_id': request.user.id})
    else:
        return Response({'is_admin': False, 'user_id': request.user.id})


@extend_schema(
    summary="Add New User",
    description="Create a new user account (Admin only)",
    tags=["User Management"]
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_user(request):
    """Add a new user (admin only)"""
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Delete User",
    description="Delete a user account (Admin only)",
    tags=["User Management"]
)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id_to_delete):
    """Delete a user (admin only)"""
    try:
        user_to_delete = User.objects.get(id=user_id_to_delete)
        if user_to_delete.id == request.user.id:
            return Response(
                {'error': 'Cannot delete yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        user_to_delete.delete()
        return Response({'message': 'User deleted successfully'})
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
