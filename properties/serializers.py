from rest_framework import serializers
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for Property model"""
    
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class PropertyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating properties"""
    
    class Meta:
        model = Property
        fields = [
            'reference', 'title', 'category', 'price', 'square_meters',
            'region', 'town', 'street_address', 'address_city', 'address_state', 'address_country',
            'bedrooms', 'bathrooms', 'land_area', 'built_up',
            'description', 'photos', 'main_image', 'features',
            'platform', 'link', 'energy_rating',
            'company_id', 'company_name', 'property_created_at', 'on_off', 'entity_id'
        ]
    
    def create(self, validated_data):
        # Check if property with same reference exists and update it
        reference = validated_data.get('reference')
        if reference:
            try:
                existing_property = Property.objects.get(reference=reference)
                # Update existing property
                for attr, value in validated_data.items():
                    setattr(existing_property, attr, value)
                existing_property.save()
                return existing_property
            except Property.DoesNotExist:
                pass
        
        # Create new property
        return Property.objects.create(**validated_data)


class PropertyUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating properties"""
    
    class Meta:
        model = Property
        fields = [
            'title', 'category', 'price', 'square_meters',
            'region', 'town', 'street_address', 'address_city', 'address_state', 'address_country',
            'bedrooms', 'bathrooms', 'land_area', 'built_up',
            'description', 'photos', 'main_image', 'features',
            'platform', 'link', 'energy_rating',
            'company_id', 'company_name', 'property_created_at', 'on_off', 'entity_id'
        ]
