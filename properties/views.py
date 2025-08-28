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
from drf_spectacular.utils import extend_schema
from .schemas import (
    PROPERTY_CREATE_SCHEMA,
    PROPERTY_LIST_SCHEMA,
    PROPERTY_DETAIL_SCHEMA,
    PROPERTY_UPDATE_SCHEMA,
    PROPERTY_DELETE_SCHEMA,
    PROPERTY_BY_REFERENCE_SCHEMA,
    ALL_REGIONS_SCHEMA,
    PATCH_PROPERTY_SCHEMA,
    BOT_SCRAPERS_SCHEMA,
    RUN_BOT_SCRAPER_SCHEMA,
    RUN_ALL_SCRAPERS_SCHEMA
)
import logging
from .pagination import PropertyPagination

logger = logging.getLogger(__name__)


@extend_schema(**PROPERTY_CREATE_SCHEMA)
class PropertyCreateView(generics.CreateAPIView):
    """Create a new property or update if reference number exists"""
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


@extend_schema(**PROPERTY_LIST_SCHEMA)
class PropertyListView(generics.ListAPIView):
    """List properties with filtering and pagination"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filterset_class = PropertyFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['price', 'square_meters', 'created_at', 'updated_at']
    ordering = ['-created_at']
    pagination_class = PropertyPagination


@extend_schema(**PROPERTY_DETAIL_SCHEMA)
class PropertyDetailView(generics.RetrieveAPIView):
    """Retrieve a specific property by ID"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


@extend_schema(**PROPERTY_UPDATE_SCHEMA)
class PropertyUpdateView(generics.UpdateAPIView):
    """Update a specific property"""
    queryset = Property.objects.all()
    serializer_class = PropertyUpdateSerializer


@extend_schema(**PROPERTY_DELETE_SCHEMA)
class PropertyDeleteView(generics.DestroyAPIView):
    """Delete a specific property"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Property deleted successfully"}, status=status.HTTP_200_OK)


@extend_schema(**PROPERTY_BY_REFERENCE_SCHEMA)
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


@extend_schema(**ALL_REGIONS_SCHEMA)
@api_view(['GET'])
def get_all_regions(request):
    """Get all unique regions"""
    regions = Property.objects.values_list('region', flat=True).distinct()
    return Response(list(regions))


@extend_schema(**PATCH_PROPERTY_SCHEMA)
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


@extend_schema(**BOT_SCRAPERS_SCHEMA)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_bot_scrapers(request):
    """Get list of available bot scrapers (Admin only)"""
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


@extend_schema(**RUN_BOT_SCRAPER_SCHEMA)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def run_bot_scraper(request):
    """Run a specific bot scraper (Admin only)"""
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


@extend_schema(**RUN_ALL_SCRAPERS_SCHEMA)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def run_all_scrapers(request):
    """Run all available scrapers (Admin only)"""
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
