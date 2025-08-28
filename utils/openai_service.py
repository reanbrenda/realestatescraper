import openai
from django.conf import settings
from django.core.cache import cache


class OpenAIService:
    """OpenAI service for property analysis and generation"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if self.api_key:
            openai.api_key = self.api_key
    
    def analyze_property_description(self, description):
        """Analyze property description and extract key features"""
        if not self.api_key:
            return None
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a real estate expert. Analyze the property description and extract key features, amenities, and characteristics."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this property description: {description}"
                    }
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing property description: {e}")
            return None
    
    def generate_property_summary(self, property_data):
        """Generate a summary for a property"""
        if not self.api_key:
            return None
        
        try:
            # Create a prompt from property data
            prompt = f"""
            Create a compelling summary for this property:
            - Title: {property_data.get('title', 'N/A')}
            - Location: {property_data.get('region', 'N/A')}, {property_data.get('town', 'N/A')}
            - Price: €{property_data.get('price', 'N/A'):,.0f}
            - Size: {property_data.get('square_meters', 'N/A')} m²
            - Bedrooms: {property_data.get('bedrooms', 'N/A')}
            - Bathrooms: {property_data.get('bathrooms', 'N/A')}
            - Description: {property_data.get('description', 'N/A')}
            
            Write a 2-3 sentence summary that highlights the key selling points.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a real estate marketing expert. Write compelling property summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating property summary: {e}")
            return None
    
    def suggest_property_features(self, description):
        """Suggest additional features based on property description"""
        if not self.api_key:
            return []
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a real estate expert. Suggest relevant features that might be present in this type of property."
                    },
                    {
                        "role": "user",
                        "content": f"Based on this description, what features might this property have? {description}"
                    }
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            # Parse response into a list of features
            features_text = response.choices[0].message.content
            features = [feature.strip() for feature in features_text.split('\n') if feature.strip()]
            return features
        except Exception as e:
            print(f"Error suggesting features: {e}")
            return []
    
    def get_cached_response(self, cache_key):
        """Get cached OpenAI response"""
        return cache.get(cache_key)
    
    def cache_response(self, cache_key, response, timeout=3600):
        """Cache OpenAI response"""
        cache.set(cache_key, response, timeout=timeout)
