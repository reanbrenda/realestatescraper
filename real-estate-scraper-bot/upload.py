import ast
import json
import os

import requests
from dotenv import load_dotenv

files = [
    "web_5_1_data.json",
]


def login_to_api(api_url):
    """Authenticate with the API and return the session with cookies"""
    session = requests.Session()

    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")

    if not username or not password:
        raise ValueError(
            "API_USERNAME or API_PASSWORD not found in environment variables"
        )

    credentials = {"username": username, "password": password}

    try:
        response = session.post(
            f"{api_url}/auth/login",
            json=credentials,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

        token = response.json().get("access_token")
        if token:
            session.headers.update({"Authorization": token})

        return session
    except requests.exceptions.RequestException as e:
        print("Failed to login to API:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        if hasattr(e, "response") and hasattr(e.response, "text"):
            print(f"Response text: {e.response.text}")
        raise


def transform_property_data(raw_property):
    """Transform scraped property data to match API schema"""
    
    def clean_value(value, field_name):
        """Clean and validate field values"""
        if value is None or value == "None" or value == "":
            return None
        if isinstance(value, str) and value.strip() == "":
            return None
        return value
    
    def safe_float(value, field_name):
        """Safely convert value to float"""
        if value is None or value == "None" or value == "":
            return None
        try:
            if isinstance(value, str):
                value = value.strip()
                if value == "" or value == "None":
                    return None
            return float(value) if value != 0 else 0.0
        except (ValueError, TypeError):
            print(f"Warning: Could not convert {field_name} '{value}' to float for property {raw_property.get('title', 'Unknown')}")
            return None
    
    def safe_int(value, field_name):
        """Safely convert value to int"""
        if value is None or value == "None" or value == "":
            return None
        try:
            if isinstance(value, str):
                value = value.strip()
                if value == "" or value == "None":
                    return None
            return int(float(value)) if value != 0 else 0
        except (ValueError, TypeError):
            print(f"Warning: Could not convert {field_name} '{value}' to int for property {raw_property.get('title', 'Unknown')}")
            return None
    
    # Handle photos array
    try:
        if isinstance(raw_property["allImages"], str):
            # Try to safely evaluate the string as a Python literal
            photos = ast.literal_eval(raw_property["allImages"])
            # Filter out the SVG placeholder images
            photos = [img for img in photos if not img.startswith("data:image/svg+xml")]
        else:
            photos = raw_property["allImages"]
            photos = [img for img in photos if not img.startswith("data:image/svg+xml")]
    except (ValueError, SyntaxError) as e:
        print(
            f"Warning: Could not parse photos for property {raw_property.get('title', 'Unknown')}: {e}"
        )
        photos = []

    # Handle main image
    main_image = clean_value(raw_property["mainImage"], "mainImage")
    if main_image and main_image.startswith("data:image/svg+xml"):
        main_image = photos[0] if photos else None

    # Ensure required fields have valid values
    title = clean_value(raw_property["title"], "title")
    if not title:
        title = f"Property from {raw_property['platform']}"
    
    location = clean_value(raw_property["location"], "location")
    if not location:
        location = "Mallorca, Spain"  # Default location
    
    price = safe_float(raw_property["price"], "price")
    if price is None:
        price = 0.0  # Default price
    
    square_meters = safe_float(raw_property["livingSpace"], "livingSpace")
    if square_meters is None:
        square_meters = 0.0  # Default square meters
    
    # Create a unique reference
    try:
        url_parts = raw_property["link"].split('/')
        reference = f"{raw_property['platform']}_{url_parts[-2] if len(url_parts) > 1 else 'unknown'}"
    except:
        reference = f"{raw_property['platform']}_{hash(raw_property['link'])}"
    
    return {
        "reference": reference,
        "platform": raw_property["platform"],
        "link": raw_property["link"],
        "region": location,
        "town": location,
        "title": title,
        "category": clean_value(raw_property["category"], "category"),
        "price": price,
        "square_meters": square_meters,
        "land_area": safe_float(raw_property["landArea"], "landArea"),
        "built_up": safe_float(raw_property["builtUp"], "builtUp"),
        "bedrooms": safe_int(raw_property["bedrooms"], "bedrooms"),
        "bathrooms": safe_int(raw_property["bathrooms"], "bathrooms"),
        "description": clean_value(raw_property["description"], "description"),
        "photos": photos,
        "main_image": main_image,
    }


def upload_json_data():
    # Load environment variables
    load_dotenv()   
    base_path=os.path.dirname(os.path.abspath(__file__))

    # Get upload URL from environment variables
    api_url = os.getenv("API_URL")
    if not api_url:
        raise ValueError("API_URL not found in environment variables")

    # Login to API first
    session = login_to_api(api_url)

    # Ask for the JSON file name
    file_input = (
        input("Please enter the JSON file name (or 'all' for all files): ")
        .strip()
        .lower()
    )

    # Determine which files to process
    files_to_process = files if file_input == "all" else [file_input]

    total_success = 0
    total_errors = 0
    # Process each file
    for file_name in files_to_process:
        file_name=os.path.join(base_path, file_name)
        print(file_name)
        print(f"\nProcessing file: {file_name}")
        # Read JSON file
        try:
            with open(file_name,"r",encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Error: {file_name} file not found")
            continue
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {file_name}")
            continue

        # Make POST request for each property
        headers = {"Content-Type": "application/json"}
        success_count = 0
        error_count = 0

        for raw_property in data:
            try:
                # Transform the data to match API schema
                property_data = transform_property_data(raw_property)

                # Use the authenticated session for making requests
                response = session.post(
                    f"{api_url}/properties", json=property_data, headers=headers
                )
                response.raise_for_status()
                success_count += 1
                print(
                    f"Successfully uploaded property: {property_data.get('title', 'Unknown')} ({response.status_code})"
                )

            except requests.exceptions.RequestException as e:
                error_count += 1
                print("\nError uploading property:")
                print(f"Title: {raw_property.get('title', 'Unknown')}")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {str(e)}")
                if hasattr(e, "response") and hasattr(e.response, "text"):
                    print(f"Response text: {e.response.text}")
                print(f"URL: {api_url}/properties")
                print("Request payload:", json.dumps(property_data, indent=2))
                print("-------------------")

        print(f"\nCompleted {file_name}:")
        print(
            f"Successfully uploaded {success_count} properties with {error_count} errors"
        )

        total_success += success_count
        total_errors += error_count

    print(f"\nAll uploads complete!")
    print(f"Total properties uploaded: {total_success}")
    print(f"Total errors: {total_errors}")


if __name__ == "__main__":
    upload_json_data()
