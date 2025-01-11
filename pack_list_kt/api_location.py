from django.conf import settings
from admin_kt.models import Location
import requests

def get_location(city, country):
    # Check if location exists in the database
    location = Location.objects.filter(city=city, country=country).first()
    if location:
        return location

    # Fetch from OpenCage API
    api_url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        'q': f"{city}, {country}",
        'key': settings.OPENCAGE_API_KEY
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            # Extract latitude and longitude
            latitude = data['results'][0]['geometry']['lat']
            longitude = data['results'][0]['geometry']['lng']
            # Save to database
            location = Location.objects.create(
                city=city,
                country=country,
                latitude=latitude,
                longitude=longitude
            )
            return location
    return None