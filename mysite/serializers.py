from rest_framework import serializers

from mysite.models import AirQualityData, Country

class AirQualityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQualityData
        fields = '__all__'

class CountryAirQualitySerializer(serializers.Serializer):
    country = serializers.CharField()
    average_aqi = serializers.FloatField()
    average_co = serializers.FloatField()
    average_no = serializers.FloatField()
    average_no2 = serializers.FloatField()
    average_o3 = serializers.FloatField()
    average_so2 = serializers.FloatField()
    average_pm2_5 = serializers.FloatField()
    average_pm10 = serializers.FloatField()
    average_nh3 = serializers.FloatField()
