import os
import sys
import requests
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import authenticate

class BotIntegrationService:
    """Service for integrating with the existing real estate scraper bot"""
    
    def __init__(self):
        # TEMPORARILY HARDCODED FOR TESTING please rember not push this to prod create env
        self.api_url = 'http://127.0.0.1:8000/api'  
        self.username = 'testuser' 
        self.password = 'testpass123'  
        self.session = None
        self.running_from_django = True 
        
        # Configuration loaded from environment variables
        
        self.bot_dir = os.path.join(settings.BASE_DIR, 'real-estate-scraper-bot')
        
        if not os.path.exists(self.bot_dir):
            possible_paths = [
                os.path.join(settings.BASE_DIR, 'real-estate-scraper-bot'),
                os.path.join(settings.BASE_DIR.parent, 'real-estate-scraper-bot'),
                '/app/real-estate-scraper-bot',
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.bot_dir = path
                    break
        
        if self.bot_dir and os.path.exists(self.bot_dir):
            if self.bot_dir not in sys.path:
                sys.path.insert(0, self.bot_dir)
        else:
            for root, dirs, files in os.walk(settings.BASE_DIR):
                if 'real-estate-scraper-bot' in dirs:
                    self.bot_dir = os.path.join(root, 'real-estate-scraper-bot')
                    if self.bot_dir not in sys.path:
                        sys.path.insert(0, self.bot_dir)
                    break
    
    def authenticate(self):
        """Authenticate with Django API and return session"""
        # If running from Django, skip HTTP authentication
        if self.running_from_django:
            return True
            
        if self.session is None:
            self.session = requests.Session()
        
        try:
            credentials = {
                "username": self.username,
                "password": self.password
            }
            
            login_url = f"{self.api_url}/auth/login/"
            
            response = self.session.post(
                login_url,
                json=credentials,
                headers={"Content-Type": "application/json"},
            )
            
            response.raise_for_status()
            
            data = response.json()
            token = data.get("access")
            
            if token:
                self.session.headers.update({"Authorization": f"Bearer {token}"})
                return True
            else:
                return False
                
        except requests.exceptions.RequestException as e:
            return False
        except Exception as e:
            return False
    
    def upload_property(self, property_data):
        """Upload a single property to Django API"""
        # If running from Django, use ORM directly
        if self.running_from_django:
            try:
                from properties.models import Property
                from django.db import transaction
                
                # Map scraper data to Django model fields
                mapped_data = self._map_scraper_data_to_model(property_data)
                
                reference = mapped_data.get('reference')
                if not reference:
                    return False
                
                with transaction.atomic():
                    # Check if property exists by reference
                    try:
                        existing_property = Property.objects.get(reference=reference)
                        # Update existing property
                        for field, value in mapped_data.items():
                            if hasattr(existing_property, field) and value is not None:
                                setattr(existing_property, field, value)
                        existing_property.save()
                        return True
                    except Property.DoesNotExist:
                        # Create new property
                        new_property = Property(**mapped_data)
                        new_property.save()
                        return True
                        
            except Exception as e:
                return False
        
        # Fallback to HTTP API for external usage
        if not self.authenticate():
            return False
        
        try:
            reference = property_data.get('reference')
            if reference:
                response = self.session.get(
                    f"{self.api_url}/properties/reference/{reference}/"
                )
                
                if response.status_code == 200:
                    property_id = response.json().get('id')
                    update_response = self.session.put(
                        f"{self.api_url}/properties/{property_id}/update/",
                        json=property_data,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if update_response.status_code == 200:
                        return True
                    else:
                        return False
                else:
                    create_response = self.session.post(
                        f"{self.api_url}/properties/create/",
                        json=property_data,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if create_response.status_code in [200, 201]:
                        return True
                    else:
                        return False
            else:
                return False
                
        except Exception as e:
            return False
    
    def _map_scraper_data_to_model(self, property_data):
        """Map scraper data structure to Django Property model fields"""
        try:
            mapped_data = {}
            
            # Map reference (Property ID -> reference)
            if 'Property ID' in property_data:
                mapped_data['reference'] = str(property_data['Property ID'])
            elif 'reference' in property_data:
                mapped_data['reference'] = str(property_data['reference'])
            
            # Map title
            if 'title' in property_data and property_data['title']:
                mapped_data['title'] = str(property_data['title'])
            
            # Map category
            if 'category' in property_data and property_data['category']:
                mapped_data['category'] = str(property_data['category'])
            
            # Map price
            if 'price' in property_data and property_data['price']:
                try:
                    mapped_data['price'] = float(property_data['price'])
                except (ValueError, TypeError):
                    mapped_data['price'] = 0.0
            
            # Map square meters (livingSpace -> square_meters)
            if 'livingSpace' in property_data and property_data['livingSpace']:
                try:
                    mapped_data['square_meters'] = float(property_data['livingSpace'])
                except (ValueError, TypeError):
                    mapped_data['square_meters'] = 0.0
            elif 'square_meters' in property_data and property_data['square_meters']:
                try:
                    mapped_data['square_meters'] = float(property_data['square_meters'])
                except (ValueError, TypeError):
                    mapped_data['square_meters'] = 0.0
            
            # Map region and town (location -> region, extract town if possible)
            if 'location' in property_data and property_data['location']:
                location = str(property_data['location'])
                # Split location into region and town if it contains commas or newlines
                if ',' in location or '\n' in location:
                    parts = location.replace('\n', ',').split(',')
                    mapped_data['region'] = parts[0].strip()
                    if len(parts) > 1:
                        mapped_data['town'] = parts[1].strip()
                else:
                    mapped_data['region'] = location
            elif 'region' in property_data and property_data['region']:
                mapped_data['region'] = str(property_data['region'])
            
            # Map town if not already set
            if 'town' not in mapped_data and 'town' in property_data and property_data['town']:
                mapped_data['town'] = str(property_data['town'])
            
            # Map bedrooms
            if 'bedrooms' in property_data and property_data['bedrooms']:
                try:
                    mapped_data['bedrooms'] = int(property_data['bedrooms'])
                except (ValueError, TypeError):
                    pass
            
            # Map bathrooms
            if 'bathrooms' in property_data and property_data['bathrooms']:
                try:
                    mapped_data['bathrooms'] = int(property_data['bathrooms'])
                except (ValueError, TypeError):
                    pass
            
            # Map land area
            if 'landArea' in property_data and property_data['landArea']:
                try:
                    mapped_data['land_area'] = float(property_data['landArea'])
                except (ValueError, TypeError):
                    pass
            
            # Map built up area
            if 'builtUp' in property_data and property_data['builtUp']:
                try:
                    mapped_data['built_up'] = float(property_data['builtUp'])
                except (ValueError, TypeError):
                    pass
            
            # Map description
            if 'description' in property_data and property_data['description']:
                mapped_data['description'] = str(property_data['description'])
            
            # Map photos (allImages -> photos)
            if 'allImages' in property_data and property_data['allImages']:
                if isinstance(property_data['allImages'], list):
                    mapped_data['photos'] = property_data['allImages']
                else:
                    mapped_data['photos'] = [str(property_data['allImages'])]
            elif 'photos' in property_data and property_data['photos']:
                mapped_data['photos'] = property_data['photos']
            
            # Map main image
            if 'mainImage' in property_data and property_data['mainImage']:
                mapped_data['main_image'] = str(property_data['mainImage'])
            elif 'main_image' in property_data and property_data['main_image']:
                mapped_data['main_image'] = str(property_data['main_image'])
            
            # Map platform
            if 'platform' in property_data and property_data['platform']:
                mapped_data['platform'] = str(property_data['platform'])
            
            # Map link
            if 'link' in property_data and property_data['link']:
                mapped_data['link'] = str(property_data['link'])
            
            # Set default values for required fields if missing
            if 'reference' not in mapped_data:
                mapped_data['reference'] = f"scraper_{hash(str(property_data))}"
            
            if 'title' not in mapped_data:
                mapped_data['title'] = "Property from scraper"
            
            if 'price' not in mapped_data:
                mapped_data['price'] = 0.0
            
            if 'square_meters' not in mapped_data:
                mapped_data['square_meters'] = 0.0
            
            if 'region' not in mapped_data:
                mapped_data['region'] = "Unknown"
            
            if 'platform' not in mapped_data:
                mapped_data['platform'] = "scraper"
            
            if 'link' not in mapped_data:
                mapped_data['link'] = "#"
            
            return mapped_data
            
        except Exception as e:
            # Return minimal required data
            return {
                'reference': f"scraper_{hash(str(property_data))}",
                'title': "Property from scraper",
                'price': 0.0,
                'square_meters': 0.0,
                'region': "Unknown",
                'platform': "scraper",
                'link': "#"
            }
    
    def _import_scraper_module(self, scraper_name):
        """Import a scraper module from the scrapers directory"""
        try:
            import importlib.util
            import os
            
            # Construct the full path to the scraper file
            scraper_file_path = os.path.join(self.bot_dir, 'scrapers', f"{scraper_name}.py")
            
            if not os.path.exists(scraper_file_path):
                return None
            
            # Load the module from the file path
            spec = importlib.util.spec_from_file_location(scraper_name, scraper_file_path)
            if spec is None:
                return None
            
            module = importlib.util.module_from_spec(spec)
            if module is None:
                return None
            
            # Execute the module
            spec.loader.exec_module(module)
            
            return module
            
        except Exception as e:
            return None
    
    def get_available_scrapers(self):
        """Get list of available scrapers"""
        try:
            if not self.authenticate():
                return []
            
            scrapers = []
            scrapers_dir = os.path.join(self.bot_dir, 'scrapers')
            
            if os.path.exists(scrapers_dir):
                for file in os.listdir(scrapers_dir):
                    if file.startswith('test_scraping') and file.endswith('.py'):
                        scraper_name = file.replace('.py', '')
                        scrapers.append(scraper_name)
            
            return scrapers
            
        except Exception as e:
            return []
    
    def run_scraper(self, scraper_name, upload_to_django=True, limit_properties=10):
        """Run a specific scraper"""
        try:
            if not self.authenticate():
                return {"success": False, "error": "Authentication failed"}
            
            scrapers = self.get_available_scrapers()
            if scraper_name not in scrapers:
                return {"success": False, "error": f"Scraper {scraper_name} not found"}
            
            # Import the scraper module properly
            scraper_module = self._import_scraper_module(scraper_name)
            if not scraper_module:
                return {"success": False, "error": f"Failed to import scraper module {scraper_name}"}
            
            if hasattr(scraper_module, 'run_scraper'):
                result = scraper_module.run_scraper(limit_properties)
                
                if upload_to_django and result.get('properties'):
                    uploaded = 0
                    updated = 0
                    
                    for i, property_data in enumerate(result['properties']):
                        if self.upload_property(property_data):
                            if property_data.get('reference') or property_data.get('Property ID'):
                                updated += 1
                            else:
                                uploaded += 1
                    
                    return {
                        "success": True,
                        "message": f"Bot scraper {scraper_name} completed successfully",
                        "scraper": scraper_name,
                        "uploaded_properties": uploaded,
                        "updated_properties": updated,
                        "total_processed": len(result['properties'])
                    }
                else:
                    return {
                        "success": True,
                        "message": f"Bot scraper {scraper_name} completed",
                        "scraper": scraper_name,
                        "properties_found": len(result.get('properties', []))
                    }
            else:
                # Handle scrapers that don't have run_scraper method but execute main logic
                
                # Check if the module has homesData (the scraped properties)
                if hasattr(scraper_module, 'homesData'):
                    properties = scraper_module.homesData
                    
                    if limit_properties and len(properties) > limit_properties:
                        properties = properties[:limit_properties]
                    
                    if upload_to_django and properties:
                        uploaded = 0
                        updated = 0
                        
                        for i, property_data in enumerate(properties):
                            if self.upload_property(property_data):
                                if property_data.get('reference') or property_data.get('Property ID'):
                                    updated += 1
                                else:
                                    uploaded += 1
                        
                        return {
                            "success": True,
                            "message": f"Bot scraper {scraper_name} completed successfully",
                            "scraper": scraper_name,
                            "uploaded_properties": uploaded,
                            "updated_properties": updated,
                            "total_processed": len(properties)
                        }
                    else:
                        return {
                            "success": True,
                            "message": f"Bot scraper {scraper_name} completed",
                            "scraper": scraper_name,
                            "properties_found": len(properties)
                        }
                else:
                    return {"success": False, "error": f"Scraper {scraper_name} has no run_scraper method or homesData"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_all_scrapers(self, upload_to_django=True, limit_properties=10):
        """Run all available scrapers"""
        try:
            scrapers = self.get_available_scrapers()
            if not scrapers:
                return {"success": False, "error": "No scrapers found"}
            
            results = []
            for scraper_name in scrapers:
                try:
                    result = self.run_scraper(scraper_name, upload_to_django, limit_properties)
                    results.append({
                        'scraper': scraper_name,
                        'success': result.get('success', False),
                        'uploaded': result.get('uploaded_properties', 0),
                        'updated': result.get('updated_properties', 0),
                        'error': result.get('error')
                    })
                except Exception as e:
                    results.append({
                        'scraper': scraper_name,
                        'success': False,
                        'error': str(e)
                    })
            
            return {
                "success": True,
                "message": "All scrapers completed",
                "results": results,
                "total_scrapers": len(scrapers)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
