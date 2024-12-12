import requests
from django.core.management.base import BaseCommand
from mysite.models import AirQualityData, Country  # Update 'mysite' with your app name
from datetime import datetime
from django.utils import timezone


class Command(BaseCommand):
    help = 'Fetch air pollution data for all countries and save to database'

    def handle(self, *args, **kwargs):
        # Define API details
        API_URL = "https://api.openweathermap.org/data/2.5/air_pollution/history"
        START, END = 1702084447, 1733706847  # Replace with appropriate timestamps
        API_KEY = "6962f291eda668b770711b1263097cc3"  # Replace with your API key

        # Fetch all countries
        countries = Country.objects.all()
        # countries = Country.objects.filter(name__in=[])
        total_records_added = 0
        total_records_skipped = 0

        for country in countries:
            lat, lon = country.latitude, country.longitude
            url = f"{API_URL}?lat={lat}&lon={lon}&start={START}&end={END}&appid={API_KEY}"

            try:
                # Fetch data from the API
                response = requests.get(url)
                response.raise_for_status()  # Raise exception for HTTP errors
                data = response.json()

                records_added = 0
                records_skipped = 0

                # Process and save data
                for item in data.get('list', []):
                    # dt = datetime.utcfromtimestamp(item['dt'])
                    aqi = item['main']['aqi']
                    components = item['components']
                    dt = timezone.make_aware(datetime.utcfromtimestamp(item["dt"]))
                    # Check for duplicates (same dt and country)
                    if not AirQualityData.objects.filter(dt=dt, country=country).exists():
                        AirQualityData.objects.create(
                            dt=dt,
                            aqi=aqi,
                            co=components.get('co', 0),
                            no=components.get('no', 0),
                            no2=components.get('no2', 0),
                            o3=components.get('o3', 0),
                            so2=components.get('so2', 0),
                            pm2_5=components.get('pm2_5', 0),
                            pm10=components.get('pm10', 0),
                            nh3=components.get('nh3', 0),
                            country=country
                        )
                        records_added += 1
                        print(dt,country,":- record added")
                    else:
                        records_skipped += 1
                        print(dt,country,":- record skipped")
                    print(dt,country)
                # Log results for the current country
                self.stdout.write(f"Country: {country.name} - Added: {records_added}, Skipped: {records_skipped}")
                print(f"Country: {country.name} - Added: {records_added}, Skipped: {records_skipped}")
                total_records_added += records_added
                total_records_skipped += records_skipped

            except requests.exceptions.RequestException as e:
                self.stderr.write(f"Failed to fetch data for {country.name}. Error: {e}")
                print(f"Failed to fetch data for {country.name}. Error: {e}")
        # Final summary
        self.stdout.write(f"Total records added: {total_records_added}")
        self.stdout.write(f"Total records skipped: {total_records_skipped}")
