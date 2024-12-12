import requests
from datetime import datetime
from celery import shared_task
from mysite.models import AirQualityData, Country  # Update 'mysite' with your app name

@shared_task
def fetch_data_periodically():
    """
    Fetch air pollution data from OpenWeatherMap API for all countries and save it to the database.
    """
    # API details
    API_URL = "https://api.openweathermap.org/data/2.5/air_pollution/history"
    START, END = 1702084447, 1733706847  # Replace with appropriate timestamps
    API_KEY = "6962f291eda668b770711b1263097cc3"  # Replace with your API key

    # Fetch all countries
    countries = Country.objects.all()
    total_records_added = 0
    total_records_skipped = 0

    for country in countries:
        # Build request URL for each country
        lat, lon = country.latitude, country.longitude
        url = f"{API_URL}?lat={lat}&lon={lon}&start={START}&end={END}&appid={API_KEY}"

        try:
            # Fetch data from API
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()

            records_added = 0
            records_skipped = 0

            # Process and save data
            for item in data.get("list", []):
                dt = datetime.utcfromtimestamp(item["dt"])  # Convert Unix timestamp to DateTime
                aqi = item["main"]["aqi"]
                components = item["components"]

                # Check if an entry with the same 'dt' and country already exists
                if AirQualityData.objects.filter(dt=dt, country=country).exists():
                    records_skipped += 1
                else:
                    AirQualityData.objects.create(
                        dt=dt,
                        aqi=aqi,
                        co=components.get("co", 0),
                        no=components.get("no", 0),
                        no2=components.get("no2", 0),
                        o3=components.get("o3", 0),
                        so2=components.get("so2", 0),
                        pm2_5=components.get("pm2_5", 0),
                        pm10=components.get("pm10", 0),
                        nh3=components.get("nh3", 0),
                        country=country
                    )
                    records_added += 1

            # Log results for the current country
            print(f"Country: {country.name} - Added: {records_added}, Skipped: {records_skipped}")
            total_records_added += records_added
            total_records_skipped += records_skipped

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for {country.name}. Error: {e}")

    # Final summary
    print(f"Total records added: {total_records_added}")
    print(f"Total records skipped: {total_records_skipped}")
