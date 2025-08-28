#!/usr/bin/env python3
"""
Real Estate Scraper Runner
Command-line interface to run property scrapers and optionally upload results to Django API.
"""

import argparse
import json
import os
import sys
import importlib.util
from pathlib import Path

# Add bot directory to Python path
BOT_DIR = Path(__file__).parent / 'real-estate-scraper-bot'
SCRAPERS_DIR = BOT_DIR / 'scrapers'

if not BOT_DIR.exists():
    print(f"Error: Bot directory not found at {BOT_DIR}")
    sys.exit(1)

if not SCRAPERS_DIR.exists():
    print(f"Error: Scrapers directory not found at {SCRAPERS_DIR}")
    sys.exit(1)

sys.path.insert(0, str(BOT_DIR))
sys.path.insert(0, str(SCRAPERS_DIR))


def get_available_scrapers():
    """Get list of available scraper modules"""
    scrapers = []
    for file in os.listdir(SCRAPERS_DIR):
        if file.startswith('test_scraping') and file.endswith('.py'):
            scraper_name = file.replace('.py', '')
            scrapers.append(scraper_name)
    return scrapers


def run_scraper(scraper_name, limit_properties=None):
    """Run a specific scraper"""
    try:
        spec = importlib.util.spec_from_file_location(
            scraper_name, 
            SCRAPERS_DIR / f"{scraper_name}.py"
        )
        scraper_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(scraper_module)
        
        if hasattr(scraper_module, 'run_scraper'):
            result = scraper_module.run_scraper(limit_properties)
            return result
        else:
            if hasattr(scraper_module, 'homesData'):
                properties = scraper_module.homesData
                if limit_properties:
                    properties = properties[:limit_properties]
                
                return {
                    "success": True,
                    "scraper": scraper_name,
                    "properties": properties,
                    "total_found": len(properties)
                }
            else:
                return {
                    "success": False,
                    "error": f"Scraper {scraper_name} has no run_scraper method or homesData"
                }
                
    except Exception as e:
        return {
            "success": False,
            "error": f"Error running scraper {scraper_name}: {str(e)}"
        }


def run_all_scrapers(limit_properties=None):
    """Run all available scrapers"""
    scrapers = get_available_scrapers()
    if not scrapers:
        return {"success": False, "error": "No scrapers found"}
    
    results = []
    for scraper_name in scrapers:
        try:
            result = run_scraper(scraper_name, limit_properties)
            results.append({
                'scraper': scraper_name,
                'success': result.get('success', False),
                'properties_found': len(result.get('properties', [])),
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


def upload_to_django(properties, api_url="http://localhost:8000/api"):
    """Upload scraped properties to Django API"""
    try:
        import requests
        print(f"Would upload {len(properties)} properties to {api_url}")
        print("Note: Authentication not implemented in this script")
        return True
    except ImportError:
        print("requests library not available for Django upload")
        return False


def main():
    parser = argparse.ArgumentParser(description='Run Real Estate Property Scrapers')
    parser.add_argument('--scraper', '-s', help='Specific scraper to run')
    parser.add_argument('--all', '-a', action='store_true', help='Run all scrapers')
    parser.add_argument('--list', '-l', action='store_true', help='List available scrapers')
    parser.add_argument('--limit', '-n', type=int, help='Limit number of properties to process')
    parser.add_argument('--upload', '-u', action='store_true', help='Upload results to Django API')
    parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    
    args = parser.parse_args()
    
    if args.list:
        scrapers = get_available_scrapers()
        print("Available scrapers:")
        for scraper in scrapers:
            print(f"  - {scraper}")
        return
    
    if not args.scraper and not args.all:
        print("Error: Must specify --scraper or --all")
        parser.print_help()
        return
    
    if args.scraper:
        if args.scraper not in get_available_scrapers():
            print(f"Error: Scraper '{args.scraper}' not found")
            print("Available scrapers:", get_available_scrapers())
            return
        
        result = run_scraper(args.scraper, args.limit)
        
        if result.get('success'):
            print(f"Scraper {args.scraper} completed successfully")
            print(f"   Properties found: {len(result.get('properties', []))}")
            
            if args.upload:
                upload_to_django(result.get('properties', []))
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"   Results saved to: {args.output}")
        else:
            print(f"Scraper {args.scraper} failed: {result.get('error')}")
    
    elif args.all:
        print("Running all available scrapers...")
        result = run_all_scrapers(args.limit)
        
        if result.get('success'):
            print("All scrapers completed")
            for scraper_result in result.get('results', []):
                status = "SUCCESS" if scraper_result['success'] else "FAILED"
                print(f"   {status} {scraper_result['scraper']}: {scraper_result.get('properties_found', 0)} properties")
                if scraper_result.get('error'):
                    print(f"      Error: {scraper_result['error']}")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"   Results saved to: {args.output}")
        else:
            print(f"Error running all scrapers: {result.get('error')}")


if __name__ == "__main__":
    main()
