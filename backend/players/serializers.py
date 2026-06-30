from rest_framework import serializers
from .models import Player, PlayerStats, PlayerMatchStatus, Position
from core.serializers import CountrySerializer
from core.models import Country
from teams.serializers import TeamSerializer
from teams.models import Team
from matches.models import Match


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    nationality = CountrySerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    position = PositionSerializer(read_only=True)
    nationality_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='nationality', write_only=True
    )
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team', write_only=True,
        allow_null=True, required=False
    )
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), source='position', write_only=True,
        allow_null=True, required=False
    )

    class Meta:
        model = Player
        fields = '__all__'


class PlayerMatchStatusSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source='player', write_only=True
    )
    match_id = serializers.PrimaryKeyRelatedField(
        queryset=Match.objects.all(), source='match', write_only=True
    )

    class Meta:
        model = PlayerMatchStatus
        fields = '__all__'


class PlayerStatsSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source='player', write_only=True)
 
    match_id = serializers.PrimaryKeyRelatedField(
        queryset=Match.objects.all(), source='match', write_only=True)

    class Meta:
        model = PlayerStats
        fields = '__all__'