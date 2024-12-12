from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Country Name")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class AirQualityData(models.Model):
    dt = models.DateTimeField(verbose_name="Date and Time")
    aqi = models.FloatField(verbose_name="Air Quality Index (AQI)")
    co = models.FloatField(verbose_name="Carbon Monoxide (CO)")
    no = models.FloatField(verbose_name="Nitric Oxide (NO)")
    no2 = models.FloatField(verbose_name="Nitrogen Dioxide (NO2)")
    o3 = models.FloatField(verbose_name="Ozone (O3)")
    so2 = models.FloatField(verbose_name="Sulfur Dioxide (SO2)")
    pm2_5 = models.FloatField(verbose_name="Particulate Matter (PM2.5)")
    pm10 = models.FloatField(verbose_name="Particulate Matter (PM10)")
    nh3 = models.FloatField(verbose_name="Ammonia (NH3)")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="air_quality_data", verbose_name="Country")

    class Meta:
        verbose_name = "Air Quality Record"
        verbose_name_plural = "Air Quality Records"

    def __str__(self):
        return f"Air Quality Data on {self.dt} in {self.country.name}"
