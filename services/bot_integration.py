import os
import sys
import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class BotIntegrationService:
    """Service for integrating with the existing real estate scraper bot"""
    
    def __init__(self):
        self.api_url = getattr(settings, 'BOT_API_URL', 'http://localhost:8000/api')
        self.username = getattr(settings, 'BOT_USERNAME', 'admin')
        self.password = getattr(settings, 'BOT_PASSWORD', 'admin123')
        self.session = None
        
        # Add bot directory to Python path - look in current Django project
        self.bot_dir = os.path.join(settings.BASE_DIR, 'real-estate-scraper-bot')
        
        if not os.path.exists(self.bot_dir):
            # Try alternative paths
            possible_paths = [
                os.path.join(settings.BASE_DIR, 'real-estate-scraper-bot'),
                os.path.join(settings.BASE_DIR.parent, 'real-estate-scraper-bot'),
                '/app/real-estate-scraper-bot',  # Docker container path
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.bot_dir = path
                    break
        
        if self.bot_dir and os.path.exists(self.bot_dir):
            if self.bot_dir not in sys.path:
                sys.path.insert(0, self.bot_dir)
            logger.info(f"Bot directory found at: {self.bot_dir}")
        else:
            logger.error(f"Bot directory not found. Tried: {self.bot_dir}")
            # Try to find it anywhere in the project
            for root, dirs, files in os.walk(settings.BASE_DIR):
                if 'real-estate-scraper-bot' in dirs:
                    self.bot_dir = os.path.join(root, 'real-estate-scraper-bot')
                    if self.bot_dir not in sys.path:
                        sys.path.insert(0, self.bot_dir)
                    logger.info(f"Bot directory found at: {self.bot_dir}")
                    break
    
    def authenticate(self):
        """Authenticate with Django API and return session"""
        if self.session is None:
            self.session = requests.Session()
        
        try:
            credentials = {
                "username": self.username,
                "password": self.password
            }
            
            response = self.session.post(
                f"{self.api_url}/auth/login/",
                json=credentials,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            
            data = response.json()
            token = data.get("access")
            
            if token:
                self.session.headers.update({"Authorization": f"Bearer {token}"})
                logger.info("Successfully authenticated with Django API")
                return True
            else:
                logger.error("No access token received from Django API")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    def upload_property(self, property_data):
        """Upload a single property to Django API"""
        if not self.authenticate():
            return False
        
        try:
            # Check if property already exists by reference
            reference = property_data.get('reference')
            if reference:
                # Try to get existing property
                response = self.session.get(
                    f"{self.api_url}/properties/reference/{reference}/"
                )
                
                if response.status_code == 200:
                    # Property exists, update it
                    property_id = response.json().get('id')
                    update_response = self.session.put(
                        f"{self.api_url}/properties/{property_id}/update/",
                        json=property_data,
                        headers={"Content-Type": "application/json"},
                    )
                    
                    if update_response.status_code == 200:
                        logger.info(f"Updated property: {reference}")
                        return True
                    else:
                        logger.error(f"Failed to update property {reference}: {update_response.status_code}")
                        return False
                
                elif response.status_code == 404:
                    # Property doesn't exist, create it
                    create_response = self.session.post(
                        f"{self.api_url}/properties/create/",
                        json=property_data,
                        headers={"Content-Type": "application/json"},
                    )
                    
                    if create_response.status_code == 201:
                        logger.info(f"Created new property: {reference}")
                        return True
                    else:
                        logger.error(f"Failed to create property {reference}: {create_response.status_code}")
                        return False
                
                else:
                    logger.error(f"Unexpected response checking property {reference}: {response.status_code}")
                    return False
            
            else:
                # No reference, create new property
                create_response = self.session.post(
                    f"{self.api_url}/properties/create/",
                    json=property_data,
                    headers={"Content-Type": "application/json"},
                )
                
                if create_response.status_code == 201:
                    logger.info("Created new property without reference")
                    return True
                else:
                    logger.error(f"Failed to create property: {create_response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error uploading property: {e}")
            return False
    
    def run_scraper(self, scraper_name, upload_to_django=True, limit_properties=3):
        """Run a specific scraper and optionally upload to Django"""
        try:
            # Import the scraper module
            scraper_module = __import__(f'scrapers.{scraper_name}', fromlist=[''])
            logger.info(f"Successfully imported scraper: {scraper_name}")
            
            # Import upload functionality
            try:
                # Try to import from the bot directory
                import sys
                import os
                
                # Add bot directory to path if not already there
                bot_dir = os.path.join(settings.BASE_DIR, 'real-estate-scraper-bot')
                if bot_dir not in sys.path:
                    sys.path.insert(0, bot_dir)
                
                from upload import transform_property_data
                logger.info("Successfully imported bot upload functionality")
            except ImportError as e:
                logger.warning(f"Could not import bot upload functionality: {e}")
                transform_property_data = None
            
            # Run the scraper
            scraped_data = []
            
            if hasattr(scraper_module, 'main'):
                # Run the scraper's main function
                scraped_data = scraper_module.main()
                logger.info(f"Scraper {scraper_name} returned {len(scraped_data)} properties")
            else:
                # Try to find scraped data in the module
                scraped_data = getattr(scraper_module, 'allHomeDetails', [])
                if not scraped_data:
                    # Try to find any data variable
                    for attr_name in dir(scraper_module):
                        if not attr_name.startswith('_'):
                            attr_value = getattr(scraper_module, attr_name)
                            if isinstance(attr_value, list) and len(attr_value) > 0:
                                scraped_data = attr_value
                                break
                
                if scraped_data:
                    logger.info(f"Found {len(scraped_data)} properties in {scraper_name}")
                else:
                    logger.warning(f"No scraped data found in {scraper_name}")
                    return 0, 0
            
            # Upload to Django if requested
            uploaded_count = 0
            updated_count = 0
            
            if upload_to_django and scraped_data:
                logger.info("Starting upload to Django...")
                
                # Check if scraped_data contains URLs (strings) or property objects
                if scraped_data and isinstance(scraped_data[0], str) and scraped_data[0].startswith('http'):
                    logger.info("Detected URLs, processing each to extract property data...")
                    
                    # Process each URL to get property data
                    processed_data = []
                    for url in scraped_data[:limit_properties]:  # Use limit_properties parameter
                        try:
                            # Import the Home class to process URLs
                            Home = getattr(scraper_module, 'Home', None)
                            if Home:
                                home = Home(url)
                                property_data = home.getAll()
                                processed_data.append(property_data)
                                logger.info(f"Processed URL: {url[:80]}...")
                            else:
                                logger.warning(f"Home class not found in {scraper_name}")
                                break
                        except Exception as e:
                            logger.error(f"Error processing URL {url}: {e}")
                            continue
                    
                    scraped_data = processed_data
                    logger.info(f"Successfully processed {len(scraped_data)} URLs into property data")
                
                # Now process the property data
                for raw_property in scraped_data:
                    try:
                        # Transform the data if possible
                        if transform_property_data:
                            transformed_property = transform_property_data(raw_property)
                        else:
                            # Basic transformation as fallback
                            transformed_property = self._basic_transform(raw_property)
                        
                        # Upload to Django
                        if self.upload_property(transformed_property):
                            uploaded_count += 1
                        else:
                            # Check if it was an update
                            if transformed_property.get('reference'):
                                updated_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error processing property: {e}")
                        continue
                
                logger.info(f"Upload complete: {uploaded_count} new, {updated_count} updated")
            
            return uploaded_count, updated_count
            
        except Exception as e:
            logger.error(f"Error running scraper {scraper_name}: {e}")
            return 0, 0
    
    def _basic_transform(self, raw_property):
        """Basic transformation for scraped property data"""
        # Extract basic information
        title = raw_property.get('title', 'Unknown Property')
        price = raw_property.get('price', 0)
        location = raw_property.get('location', 'Unknown Location')
        description = raw_property.get('description', '')
        link = raw_property.get('link', '')
        platform = raw_property.get('platform', 'unknown')
        
        # Create reference from platform and link
        reference = f"{platform}_{hash(link) % 1000000}"
        
        return {
            'reference': reference,
            'platform': platform,
            'link': link,
            'region': location,
            'town': location,
            'title': title,
            'price': float(price) if price else 0.0,
            'description': description,
            'photos': raw_property.get('allImages', []),
            'main_image': raw_property.get('mainImage', ''),
            'category': raw_property.get('category', 'house'),
            'square_meters': float(raw_property.get('livingSpace', 0)) if raw_property.get('livingSpace') else None,
            'bedrooms': int(raw_property.get('bedrooms', 0)) if raw_property.get('bedrooms') else None,
            'bathrooms': int(raw_property.get('bathrooms', 0)) if raw_property.get('bathrooms') else None,
            'land_area': float(raw_property.get('landArea', 0)) if raw_property.get('landArea') else None,
            'built_up': float(raw_property.get('builtUp', 0)) if raw_property.get('builtUp') else None,
        }
    
    def get_available_scrapers(self):
        """Get list of available scrapers"""
        scrapers = []
        scrapers_dir = os.path.join(self.bot_dir, 'scrapers')
        
        if os.path.exists(scrapers_dir):
            for file in os.listdir(scrapers_dir):
                if file.startswith('test_scraping') and file.endswith('.py'):
                    scraper_name = file[:-3]  # Remove .py extension
                    scrapers.append(scraper_name)
        
        return scrapers
    
    def get_scraper_status(self, scraper_name):
        """Get status and info about a specific scraper"""
        try:
            scraper_module = __import__(f'scrapers.{scraper_name}', fromlist=[''])
            
            # Get basic info
            info = {
                'name': scraper_name,
                'module': scraper_module.__name__,
                'file': scraper_module.__file__,
                'has_main': hasattr(scraper_module, 'main'),
                'attributes': [attr for attr in dir(scraper_module) if not attr.startswith('_')]
            }
            
            # Try to get sample data
            try:
                if hasattr(scraper_module, 'main'):
                    sample_data = scraper_module.main()
                    if sample_data and len(sample_data) > 0:
                        info['sample_property'] = sample_data[0]
                        info['total_properties'] = len(sample_data)
                else:
                    # Look for data variables
                    for attr_name in ['allHomeDetails', 'properties', 'data']:
                        if hasattr(scraper_module, attr_name):
                            data = getattr(scraper_module, attr_name)
                            if isinstance(data, list) and len(data) > 0:
                                info['sample_property'] = data[0]
                                info['total_properties'] = len(data)
                                break
            except Exception as e:
                info['sample_error'] = str(e)
            
            return info
            
        except Exception as e:
            return {
                'name': scraper_name,
                'error': str(e)
            }
