from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mysite.models import AirQualityData
from .serializers import AirQualityDataSerializer
from django.http import JsonResponse
from django.db.models import Avg, Q, F
from .serializers import CountryAirQualitySerializer

def air_quality_data(request):
    # Fetch data from the database
    data = AirQualityData.objects.values('dt', 'aqi', 'co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3')
    return JsonResponse(list(data), safe=False)

class AirQualityListView(APIView):
    """
    API endpoint to get all items or a range of items.
    """

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            items = AirQualityData.objects.filter(dt__range=[start_date, end_date])
        else:
            items = AirQualityData.objects.all()

        serializer = AirQualityDataSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AirQualityDetailView(APIView):
    """
    API endpoint to get a single item by ID.
    """

    def get(self, request, pk):
        try:
            item = AirQualityData.objects.get(pk=pk)
        except AirQualityData.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AirQualityDataSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CountryAirQualityAverageView(APIView):
    """
    API endpoint to get country-wise average air quality values with optional filters.
    """

    def get(self, request):
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        country_name = request.query_params.get('country')

        # Build filters dynamically
        filters = Q()
        if start_date:
            filters &= Q(dt__gte=start_date)
        if end_date:
            filters &= Q(dt__lte=end_date)
        if country_name:
            filters &= Q(country__name__iexact=country_name)

        # Query data with filters and calculate averages
        aggregated_data = (
            AirQualityData.objects.filter(filters)
            .values('country__name')  # Group by country name
            .annotate(
                average_aqi=Avg('aqi'),
                average_co=Avg('co'),
                average_no=Avg('no'),
                average_no2=Avg('no2'),
                average_o3=Avg('o3'),
                average_so2=Avg('so2'),
                average_pm2_5=Avg('pm2_5'),
                average_pm10=Avg('pm10'),
                average_nh3=Avg('nh3'),
            )
            .order_by('country__name')  # Sort by country name
        )

        # Rename `country__name` to `country` for the serializer
        renamed_data = [
            {
                "country": item["country__name"],
                "average_aqi": item["average_aqi"],
                "average_co": item["average_co"],
                "average_no": item["average_no"],
                "average_no2": item["average_no2"],
                "average_o3": item["average_o3"],
                "average_so2": item["average_so2"],
                "average_pm2_5": item["average_pm2_5"],
                "average_pm10": item["average_pm10"],
                "average_nh3": item["average_nh3"],
            }
            for item in aggregated_data
        ]

        return Response(renamed_data)
    
# Composite Pollution Index API

class MostPollutedCountryView(APIView):
    """
    API endpoint to get the most polluted country and a ranked list of countries based on pollution.
    """

    def get(self, request):
        # Aggregate data with average pollutant values
        aggregated_data = (
            AirQualityData.objects.values('country__name')
            .annotate(
                country=F('country__name'),
                average_aqi=Avg('aqi'),
                average_co=Avg('co'),
                average_no=Avg('no'),
                average_no2=Avg('no2'),
                average_o3=Avg('o3'),
                average_so2=Avg('so2'),
                average_pm2_5=Avg('pm2_5'),
                average_pm10=Avg('pm10'),
                average_nh3=Avg('nh3'),
                composite_pollution=(
                    2 * Avg('pm2_5') + 1.5 * Avg('pm10') + 1.2 * Avg('co') + 1.1 * Avg('no2')
                )  # Example composite index
            )
            .order_by('-average_aqi')  # Sort by AQI in descending order
        )

        # Determine the most polluted country
        most_polluted = aggregated_data[0] if aggregated_data else None

        return Response({
            "most_polluted_country": most_polluted,
            "ranked_countries": list(aggregated_data)
        })
