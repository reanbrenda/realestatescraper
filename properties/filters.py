import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    """Filter for Property model - matches FastAPI filtering exactly"""
    
    # Text search
    search = django_filters.CharFilter(method='filter_search')
    
    # Multiple choice filters
    region = django_filters.BaseInFilter()
    category = django_filters.BaseInFilter()
    energy_rating = django_filters.BaseInFilter()
    
    # Range filters - match API docs exactly
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    square_meters_min = django_filters.NumberFilter(field_name='square_meters', lookup_expr='gte')
    square_meters_max = django_filters.NumberFilter(field_name='square_meters', lookup_expr='lte')
    
    bedrooms = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    bathrooms = django_filters.NumberFilter(field_name='bathrooms', lookup_expr='gte')
    
    land_area_min = django_filters.NumberFilter(field_name='land_area', lookup_expr='gte')
    land_area_max = django_filters.NumberFilter(field_name='land_area', lookup_expr='lte')
    
    # Exact match filters
    platform = django_filters.CharFilter(lookup_expr='exact')
    
    # Pagination parameters
    page = django_filters.NumberFilter(method='filter_page')
    page_size = django_filters.NumberFilter(method='filter_page_size')
    
    class Meta:
        model = Property
        fields = {
            'price': ['gte', 'lte'],
            'square_meters': ['gte', 'lte'],
            'bedrooms': ['gte', 'lte'],
            'bathrooms': ['gte', 'lte'],
            'land_area': ['gte', 'lte'],
        }
    
    def filter_search(self, queryset, name, value):
        """Search in title, description, region, and town fields"""
        if value:
            return queryset.filter(
                django_filters.Q(title__icontains=value) |
                django_filters.Q(description__icontains=value) |
                django_filters.Q(region__icontains=value) |
                django_filters.Q(town__icontains=value)
            )
        return queryset
    
    def filter_page(self, queryset, name, value):
        """Handle page parameter for pagination"""
        if value and value >= 1:
            # This will be handled by Django's pagination
            return queryset
        return queryset
    
    def filter_page_size(self, queryset, name, value):
        """Handle page_size parameter for pagination"""
        if value and value >= 1 and value <= 100:
            # This will be handled by Django's pagination
            return queryset
        return queryset
