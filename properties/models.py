from django.db import models


class Property(models.Model):
    """Property model for real estate listings"""
    
    # Energy rating choices
    ENERGY_RATING_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
    ]
    
    # Basic property info
    reference = models.TextField(unique=True, null=False)  # Agent's reference number
    title = models.TextField(null=False)
    category = models.TextField(null=True, blank=True)  # house, apartment, finca, etc.
    price = models.FloatField(null=False)
    square_meters = models.FloatField(null=False)
    
    # Location info
    region = models.TextField(null=False)
    town = models.TextField(null=True, blank=True)  # Optional more specific location
    street_address = models.CharField(max_length=255, null=True, blank=True)
    address_city = models.CharField(max_length=255, null=True, blank=True)
    address_state = models.CharField(max_length=255, null=True, blank=True)
    address_country = models.CharField(max_length=255, null=True, blank=True)
    
    # Features
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    land_area = models.FloatField(null=True, blank=True)
    built_up = models.FloatField(null=True, blank=True)
    
    # Detailed information
    description = models.TextField(null=True, blank=True)
    photos = models.JSONField(default=list)  # Array of photo URLs
    main_image = models.TextField(null=True, blank=True)  # Main image URL
    features = models.TextField(null=True, blank=True)
    
    # Platform and metadata
    platform = models.TextField(null=False)
    link = models.TextField(null=False)  # URLs can be long
    energy_rating = models.CharField(max_length=1, choices=ENERGY_RATING_CHOICES, null=True, blank=True)
    
    # Client-specific fields
    company_id = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    property_created_at = models.DateTimeField(null=True, blank=True)
    on_off = models.BooleanField(null=True, blank=True)
    entity_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'properties'
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reference} - {self.title} ({self.region})"
    
    def get_absolute_url(self):
        return f"/api/properties/{self.id}/"
