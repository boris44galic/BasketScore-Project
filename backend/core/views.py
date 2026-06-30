from rest_framework import viewsets
from .models import Country, City, Hall, Season
from .serializers import CountrySerializer, CitySerializer, HallSerializer, SeasonSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related('country').all()
    serializer_class = CitySerializer


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.select_related('city').all()
    serializer_class = HallSerializer


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer