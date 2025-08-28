import os
import sys
import django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import execute_from_command_line

# Add the bot directory to Python path
BOT_DIR = os.path.join(settings.BASE_DIR.parent, 'real-estate-scraper-bot')
sys.path.insert(0, BOT_DIR)

class Command(BaseCommand):
    help = 'Run the real estate scraper bot and integrate with Django'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--scraper',
            type=str,
            default='test_scraping1',
            help='Scraper to run (default: test_scraping1)'
        )
        parser.add_argument(
            '--upload',
            action='store_true',
            help='Upload scraped data to Django database'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without saving to database'
        )
    
    def handle(self, *args, **options):
        scraper_name = options['scraper']
        upload = options['upload']
        dry_run = options['dry_run']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting bot with scraper: {scraper_name}')
        )
        
        try:
            # Check if bot directory exists
            if not os.path.exists(BOT_DIR):
                # Try to find bot directory using the service
                from services.bot_integration import BotIntegrationService
                bot_service = BotIntegrationService()
                
                if not bot_service.bot_dir:
                    raise CommandError(
                        f'Bot directory not found!\n'
                        f'Tried: {BOT_DIR}\n'
                        f'Make sure the real-estate-scraper-bot directory exists and contains scrapers/'
                    )
                else:
                    self.stdout.write(f'✅ Bot directory found at: {bot_service.bot_dir}')
            
            # Set environment variables for the bot
            os.environ.setdefault('API_URL', 'http://localhost:8000/api')
            os.environ.setdefault('API_USERNAME', 'admin')
            os.environ.setdefault('API_PASSWORD', 'admin123')
            
            # Import bot modules
            try:
                # Import the specific scraper
                scraper_module = __import__(f'scrapers.{scraper_name}', fromlist=[''])
                self.stdout.write(f'✅ Successfully imported {scraper_name}')
                
                # Import upload functionality
                import sys
                import os
                
                # Add bot directory to path
                bot_dir = os.path.join(settings.BASE_DIR, 'real-estate-scraper-bot')
                if bot_dir not in sys.path:
                    sys.path.insert(0, bot_dir)
                
                try:
                    from upload import transform_property_data, upload_json_data
                    self.stdout.write('✅ Successfully imported upload functionality')
                except ImportError:
                    self.stdout.write('⚠️  Could not import upload functionality, using fallback')
                    transform_property_data = None
                    upload_json_data = None
                
            except ImportError as e:
                raise CommandError(f'Failed to import bot modules: {e}')
            
            # Run the scraper
            self.stdout.write('🚀 Running scraper...')
            
            if hasattr(scraper_module, 'main'):
                # Run the scraper's main function
                scraped_data = scraper_module.main()
                self.stdout.write(f'✅ Scraped {len(scraped_data)} properties')
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
                    self.stdout.write(f'✅ Found {len(scraped_data)} URLs in {scraper_name}')
                    
                    # Check if we have URLs that need to be processed
                    if scraped_data and isinstance(scraped_data[0], str) and scraped_data[0].startswith('http'):
                        self.stdout.write('🔍 Processing URLs to extract property data...')
                        
                        # Import the Home class to process URLs - use the correct one for this scraper
                        try:
                            # Try to import Home from the same scraper module
                            Home = getattr(scraper_module, 'Home')
                            self.stdout.write(f'✅ Using Home class from {scraper_name}')
                        except AttributeError:
                            # Fallback to test_scraping1 if Home not found
                            try:
                                from scrapers.test_scraping1 import Home
                                self.stdout.write(f'⚠️  Using fallback Home class from test_scraping1')
                            except ImportError:
                                self.stdout.write(f'❌ Could not import fallback Home class')
                                raise CommandError(f'Home class not found in {scraper_name} and fallback failed')
                        
                        # Process each URL to get property data
                        processed_data = []
                        for i, url in enumerate(scraped_data[:3]):  # Limit to 3 properties for speed
                            try:
                                self.stdout.write(f'  Processing URL {i+1}/{min(3, len(scraped_data))}: {url[:80]}...')
                                home = Home(url)
                                property_data = home.getAll()
                                processed_data.append(property_data)
                                self.stdout.write(f'    ✅ Extracted: {property_data.get("title", "Unknown")}')
                            except Exception as e:
                                self.stdout.write(f'    ❌ Failed: {str(e)[:100]}...')
                                continue
                        
                        scraped_data = processed_data
                        self.stdout.write(f'✅ Successfully processed {len(scraped_data)} properties')
                    else:
                        self.stdout.write(f'✅ Found {len(scraped_data)} properties in {scraper_name}')
                else:
                    raise CommandError(f'No scraped data found in {scraper_name}')
            
            # Show sample data
            if scraped_data and len(scraped_data) > 0:
                sample = scraped_data[0]
                self.stdout.write(
                    self.style.SUCCESS('Sample scraped data:')
                )
                
                # Debug: Check the type and content of the sample
                self.stdout.write(f'  Sample type: {type(sample)}')
                self.stdout.write(f'  Sample content: {str(sample)[:200]}...')
                
                # Only try to show items if it's a dictionary
                if isinstance(sample, dict):
                    for key, value in list(sample.items())[:5]:  # Show first 5 fields
                        self.stdout.write(f'  {key}: {str(value)[:100]}...')
                else:
                    self.stdout.write(f'  Raw sample: {str(sample)[:200]}...')
            
            # Upload to Django if requested
            if upload and not dry_run:
                self.stdout.write('📤 Uploading properties to Django...')
                
                # Create a session and authenticate
                import requests
                session = requests.Session()
                
                # Login to get token
                login_response = session.post(
                    f"{os.environ['API_URL']}/auth/login/",
                    json={
                        "username": os.environ['API_USERNAME'],
                        "password": os.environ['API_PASSWORD']
                    },
                    headers={"Content-Type": "application/json"}
                )
                
                if login_response.status_code == 200:
                    token_data = login_response.json()
                    access_token = token_data.get('access')
                    session.headers.update({"Authorization": f"Bearer {access_token}"})
                    self.stdout.write('✅ Authenticated with Django API')
                else:
                    raise CommandError(f'Failed to authenticate: {login_response.status_code}')
                
                # Transform and upload each property
                uploaded_count = 0
                for raw_property in scraped_data:
                    try:
                        # Transform the data
                        transformed_property = transform_property_data(raw_property)
                        
                        # Upload to Django API
                        response = session.post(
                            f"{os.environ['API_URL']}/properties/create/",
                            json=transformed_property,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if response.status_code in [200, 201]:
                            uploaded_count += 1
                            self.stdout.write(f'  ✅ Uploaded: {transformed_property.get("title", "Unknown")}')
                        else:
                            self.stdout.write(f'  ❌ Failed: {transformed_property.get("title", "Unknown")} - {response.status_code}')
                            
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  ❌ Error uploading property: {e}')
                        )
                        continue
                
                self.stdout.write(
                    self.style.SUCCESS(f'Upload complete: {uploaded_count}/{len(scraped_data)} properties uploaded')
                )
            
            elif dry_run:
                self.stdout.write(
                    self.style.WARNING('DRY RUN - No data uploaded to database')
                )
            
            self.stdout.write(
                self.style.SUCCESS('Bot execution completed successfully!')
            )
            
        except Exception as e:
            raise CommandError(f'Bot execution failed: {e}')
