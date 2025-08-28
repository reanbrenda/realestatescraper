from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """Admin configuration for Property model"""
    
    list_display = [
        'reference', 'title', 'region', 'town', 'price', 'square_meters',
        'bedrooms', 'bathrooms', 'platform', 'created_at'
    ]
    
    list_filter = [
        'region', 'category', 'platform', 'energy_rating', 'created_at',
        'bedrooms', 'bathrooms'
    ]
    
    search_fields = [
        'reference', 'title', 'description', 'region', 'town',
        'street_address', 'address_city'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('reference', 'title', 'category', 'price', 'square_meters')
        }),
        ('Location', {
            'fields': ('region', 'town', 'street_address', 'address_city', 'address_state', 'address_country')
        }),
        ('Features', {
            'fields': ('bedrooms', 'bathrooms', 'land_area', 'built_up', 'energy_rating')
        }),
        ('Details', {
            'fields': ('description', 'photos', 'main_image', 'features')
        }),
        ('Platform & Metadata', {
            'fields': ('platform', 'link', 'company_id', 'company_name', 'entity_id')
        }),
        ('Status', {
            'fields': ('on_off', 'property_created_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    list_per_page = 50
    
    # Add bulk actions
    actions = ['bulk_delete_properties']
    
    def bulk_delete_properties(self, request, queryset):
        """Bulk delete selected properties"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Successfully deleted {count} properties.')
    bulk_delete_properties.short_description = "Delete selected properties"
