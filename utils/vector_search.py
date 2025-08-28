import openai
import numpy as np
from django.conf import settings
from django.core.cache import cache
from properties.models import Property
from django.db import models


class VectorSearch:
    """Vector search functionality using OpenAI embeddings"""
    
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        self.embedding_dimensions = settings.EMBEDDING_DIMENSIONS
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def get_embedding(self, text):
        """Get embedding for text using OpenAI API"""
        if not self.openai_api_key:
            return None
        
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
    
    def search_similar_properties(self, query, limit=10):
        """Search for properties similar to the query"""
        if not self.openai_api_key:
            return Property.objects.none()
        
        # Get query embedding
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return Property.objects.none()
        
        # For now, return properties with similar text content
        # In a production system, you'd store embeddings in the database
        # and perform vector similarity search
        
        # Simple text-based search as fallback
        return Property.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(region__icontains=query)
        )[:limit]
    
    def get_property_embedding(self, property_obj):
        """Get embedding for a property"""
        # Combine relevant property fields for embedding
        text = f"{property_obj.title} {property_obj.description or ''} {property_obj.region} {property_obj.category or ''}"
        return self.get_embedding(text)
    
    def cache_property_embedding(self, property_id, embedding):
        """Cache property embedding"""
        cache_key = f"property_embedding_{property_id}"
        cache.set(cache_key, embedding, timeout=3600)  # Cache for 1 hour
    
    def get_cached_embedding(self, property_id):
        """Get cached property embedding"""
        cache_key = f"property_embedding_{property_id}"
        return cache.get(cache_key)
