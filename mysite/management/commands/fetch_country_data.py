import requests
from django.core.management.base import BaseCommand
from mysite.models import Country

# OpenWeatherMap Geocoding API
API_URL = "http://api.openweathermap.org/geo/1.0/direct"
API_KEY = "6962f291eda668b770711b1263097cc3"

# List of countries
countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
    "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Canada", "United States", "United Kingdom", "India", "China", "Russia"
]

class Command(BaseCommand):
    help = "Fetch country data and store it in the database without duplicates"

    def handle(self, *args, **kwargs):
        

        for country_name in countries:
            # Check if the country already exists in the database
            if Country.objects.filter(name=country_name).exists():
                self.stdout.write(f"Country already exists: {country_name}")
                continue  # Skip to the next country

            # Fetch data from the API
            response = requests.get(API_URL, params={"q": country_name, "limit": 1, "appid": API_KEY})
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = data[0]["lat"]
                    lon = data[0]["lon"]
                    Country.objects.create(name=country_name, latitude=lat, longitude=lon)
                    self.stdout.write(f"Added country: {country_name} ({lat}, {lon})")
                else:
                    self.stderr.write(f"No data returned for {country_name}")
            else:
                self.stderr.write(f"Failed to fetch data for {country_name}: {response.status_code}")

# # Function to fetch latitude and longitude for a country
# def fetch_coordinates(country_name):
#     params = {
#         "q": country_name,
#         "limit": 1,  # Limit to one result
#         "appid": API_KEY
#     }
#     response = requests.get(API_URL, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         if data:
#             return data[0]["lat"], data[0]["lon"]
#     return None, None

# # Populate the Country table
# def populate_country_table():
#     for country in countries:
#         lat, lon = fetch_coordinates(country)
#         if lat is not None and lon is not None:
#             Country.objects.get_or_create(
#                 name=country,
#                 defaults={"latitude": lat, "longitude": lon}
#             )
#             print(f"Added: {country} ({lat}, {lon})")
#         else:
#             print(f"Failed to fetch coordinates for: {country}")

# # Run the function
# populate_country_table()
