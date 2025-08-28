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
                serializer = PropertyUpdateSerializer(existing_property, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Property.DoesNotExist:
                pass
        
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
        return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(**ALL_REGIONS_SCHEMA)
@api_view(['GET'])
def get_all_regions(request):
    """Get list of all unique regions"""
    regions = Property.objects.values_list('region', flat=True).distinct()
    return Response(list(regions))


@extend_schema(**PATCH_PROPERTY_SCHEMA)
@api_view(['PATCH'])
def patch_property(request, pk):
    """Partial update of property"""
    try:
        property_obj = Property.objects.get(pk=pk)
        serializer = PropertySerializer(property_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(**BOT_SCRAPERS_SCHEMA)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_bot_scrapers(request):
    """List available bot scrapers"""
    try:
        bot_service = BotIntegrationService()
        scrapers = bot_service.get_available_scrapers()
        return Response({
            "scrapers": scrapers,
            "total_scrapers": len(scrapers)
        })
    except Exception as e:
        logger.error(f"Error listing bot scrapers: {e}")
        return Response({"error": "Failed to list scrapers"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(**RUN_BOT_SCRAPER_SCHEMA)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def run_bot_scraper(request):
    """Run a specific bot scraper"""
    try:
        scraper_name = request.data.get('scraper_name')
        upload_to_django = request.data.get('upload_to_django', True)
        limit_properties = request.data.get('limit_properties', 10)
        
        if not scraper_name:
            return Response({"error": "scraper_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        bot_service = BotIntegrationService()
        result = bot_service.run_scraper(scraper_name, upload_to_django, limit_properties)
        
        if result.get('success'):
            return Response(result)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error running bot scraper: {e}")
        return Response({"error": "Failed to run scraper"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(**RUN_ALL_SCRAPERS_SCHEMA)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def run_all_bot_scrapers(request):
    """Run all available bot scrapers"""
    try:
        upload_to_django = request.data.get('upload_to_django', True)
        limit_properties = request.data.get('limit_properties', 10)
        
        bot_service = BotIntegrationService()
        result = bot_service.run_all_scrapers(upload_to_django, limit_properties)
        
        if result.get('success'):
            return Response(result)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error running all bot scrapers: {e}")
        return Response({"error": "Failed to run scrapers"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
