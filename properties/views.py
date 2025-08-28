from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Property
from .serializers import PropertySerializer, PropertyCreateSerializer, PropertyUpdateSerializer
from .filters import PropertyFilter
from services.bot_integration import BotIntegrationService
# OpenAPI documentation removed - views no longer have schema decorators
import logging
from .pagination import PropertyPagination

logger = logging.getLogger(__name__)


# OpenAPI documentation removed - schema defined in api_docs.py
class PropertyCreateView(generics.CreateAPIView):
    """
    Create a new property or update if reference number exists
    
    **Key Features:**
    - **Photos Field**: Accepts an array of image URLs (strings)
    - **Auto-update**: If reference exists, updates the existing property
    - **Flexible Data**: Most fields are optional except reference, title, price, square_meters, region, platform, link
    
    **Data Types:**
    - **Strings**: reference, title, category, region, town, description, platform, link
    - **Numbers**: price, square_meters, land_area, built_up
    - **Integers**: bedrooms, bathrooms
    - **Arrays**: photos (list of URL strings)
    - **Booleans**: on_off
    - **Dates**: property_created_at
    
    **Example Usage:**
    ```bash
    curl -X POST http://localhost:8000/api/properties/create/ \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{
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
      }'
    ```
    """
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer

    def create(self, request, *args, **kwargs):
        """Override create to handle update if reference exists"""
        reference = request.data.get('reference')
        if reference:
            try:
                existing_property = Property.objects.get(reference=reference)
                # Update existing property
                serializer = PropertyUpdateSerializer(existing_property, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Property.DoesNotExist:
                pass
        
        # Create new property
        return super().create(request, *args, **kwargs)


# OpenAPI documentation removed - schema defined in api_docs.py
class PropertyListView(generics.ListAPIView):
    """
    List properties with filtering and pagination
    
    **Search & Filtering:**
    - **Search**: Use `search` parameter to search in title, description, region, town
    - **Price Range**: `price_min` and `price_max` for price filtering
    - **Location**: `region` and `town` for location filtering
    - **Features**: `bedrooms`, `bathrooms` for feature filtering
    - **Platform**: `platform` to filter by source website
    - **Category**: `category` to filter by property type
    
    **Sorting:**
    - **Default**: Properties sorted by creation date (newest first)
    - **Custom**: Use `ordering` parameter (e.g., `price`, `-price`, `square_meters`)
    
    **Pagination:**
    - **Page Size**: 100 properties per page
    - **Navigation**: Use `page` parameter and follow `next`/`previous` links
    
    **Example Usage:**
    ```bash
    # Search for apartments in Palma
    curl "http://localhost:8000/api/properties/?search=palma%20apartment&region=Mallorca&category=apartment"
    
    # Filter by price and bedrooms
    curl "http://localhost:8000/api/properties/?price_min=300000&price_max=600000&bedrooms=2"
    
    # Sort by price (highest first)
    curl "http://localhost:8000/api/properties/?ordering=-price"
    ```
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filterset_class = PropertyFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['price', 'square_meters', 'created_at', 'updated_at']
    ordering = ['-created_at']
    pagination_class = PropertyPagination


class PropertyDetailView(generics.RetrieveAPIView):
    """Retrieve a specific property by ID"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PropertyUpdateView(generics.UpdateAPIView):
    """Update a specific property"""
    queryset = Property.objects.all()
    serializer_class = PropertyUpdateSerializer


class PropertyDeleteView(generics.DestroyAPIView):
    """Delete a specific property"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Property deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_property_by_reference(request, reference):
    """Get property by reference number"""
    try:
        property_obj = Property.objects.get(reference=reference)
        serializer = PropertySerializer(property_obj)
        return Response(serializer.data)
    except Property.DoesNotExist:
        return Response(
            {'error': 'Property not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def get_all_regions(request):
    """Get all unique regions"""
    regions = Property.objects.values_list('region', flat=True).distinct()
    return Response(list(regions))


@api_view(['PATCH'])
def patch_property(request, property_id):
    """PATCH endpoint to match FastAPI exactly"""
    try:
        property_obj = get_object_or_404(Property, id=property_id)
        serializer = PropertyUpdateSerializer(property_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"PATCH property error: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# OpenAPI documentation removed - schema defined in api_docs.py
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_bot_scrapers(request):
    """
    Get list of available bot scrapers (Admin only)
    
    **Response:**
    - success: Boolean indicating if the request was successful
    - scrapers: Array of scraper objects with details
    - total_scrapers: Total number of available scrapers
    
    **Example Usage:**
    ```bash
    curl -X GET http://localhost:8000/api/bot/scrapers/ \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    try:
        bot_service = BotIntegrationService()
        scrapers = bot_service.get_available_scrapers()
        
        # Get detailed info for each scraper
        scraper_details = []
        for scraper_name in scrapers:
            details = bot_service.get_scraper_status(scraper_name)
            scraper_details.append(details)
        
        return Response({
            'success': True,
            'scrapers': scraper_details,
            'total_scrapers': len(scrapers)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error getting bot scrapers: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# OpenAPI documentation removed - schema defined in api_docs.py
@api_view(['POST'])
@permission_classes([IsAdminUser])
def run_bot_scraper(request):
    """
    Run a specific bot scraper (Admin only)
    
    **Request Body:**
    - scraper_name (required): Name of the scraper to execute
    - upload_to_django (optional): Whether to upload properties to Django (default: true)
    - limit_properties (optional): Maximum properties to process (default: 3)
    
    **Response:**
    - success: Boolean indicating if the scraper ran successfully
    - message: Human-readable success message
    - scraper: Name of the executed scraper
    - uploaded_properties: Number of new properties uploaded
    - updated_properties: Number of existing properties updated
    - total_processed: Total number of properties processed
    
    **Example Usage:**
    ```bash
    curl -X POST http://localhost:8000/api/bot/run/ \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{"scraper_name": "test_scraping1", "upload_to_django": true, "limit_properties": 3}'
    ```
    """
    try:
        scraper_name = request.data.get('scraper_name', 'test_scraping1')
        upload_to_django = request.data.get('upload_to_django', True)
        limit_properties = request.data.get('limit_properties', 3)

        # Validate scraper name
        bot_service = BotIntegrationService()
        available_scrapers = bot_service.get_available_scrapers()
        
        if scraper_name not in available_scrapers:
            return Response({
                'success': False,
                'error': f'Scraper {scraper_name} not found',
                'available_scrapers': available_scrapers
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Run the scraper directly
        uploaded, updated = bot_service.run_scraper(scraper_name, upload_to_django, limit_properties)
        
        return Response({
            'success': True,
            'message': f'Bot scraper {scraper_name} completed successfully',
            'scraper': scraper_name,
            'uploaded_properties': uploaded,
            'updated_properties': updated,
            'total_processed': uploaded + updated
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Bot scraper error: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# OpenAPI documentation removed - schema defined in api_docs.py
@api_view(['POST'])
@permission_classes([IsAdminUser])
def run_all_scrapers(request):
    """
    Run all available scrapers (Admin only)
    
    **Request Body:**
    - upload_to_django (optional): Whether to upload properties to Django (default: true)
    - limit_properties (optional): Maximum properties to process per scraper (default: 3)
    
    **Response:**
    - success: Boolean indicating if all scrapers ran successfully
    - message: Human-readable success message
    - results: Array of results for each scraper
    - total_scrapers: Total number of scrapers executed
    
    **Example Usage:**
    ```bash
    curl -X POST http://localhost:8000/api/bot/run-all/ \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{"upload_to_django": true, "limit_properties": 3}'
    ```
    """
    try:
        upload_to_django = request.data.get('upload_to_django', True)
        limit_properties = request.data.get('limit_properties', 3)

        # Run all scrapers directly
        bot_service = BotIntegrationService()
        available_scrapers = bot_service.get_available_scrapers()
        
        results = []
        for scraper_name in available_scrapers:
            try:
                uploaded, updated = bot_service.run_scraper(scraper_name, upload_to_django, limit_properties)
                results.append({
                    'scraper': scraper_name,
                    'uploaded': uploaded,
                    'updated': updated,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'scraper': scraper_name,
                    'error': str(e),
                    'success': False
                })

        return Response({
            'success': True,
            'message': 'All scrapers completed',
            'results': results,
            'total_scrapers': len(available_scrapers)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Run all scrapers error: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
