from rest_framework import serializers
from .models import Team
from core.serializers import CitySerializer
from core.models import City


class TeamSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source='city', write_only=True
    )

    class Meta:
        model = Team
        fields = '__all__'
