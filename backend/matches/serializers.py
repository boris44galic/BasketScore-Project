from rest_framework import serializers
from .models import Match, Status
from teams.serializers import TeamSerializer
from teams.models import Team
from leagues.serializers import LeagueSerializer
from leagues.models import League
from core.serializers import SeasonSerializer, HallSerializer
from core.models import Season, Hall


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    league = LeagueSerializer(read_only=True)
    season = SeasonSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    hall = HallSerializer(read_only=True)

    home_team_id = serializers.PrimaryKeyRelatedField(
                    queryset=Team.objects.all(), source='home_team', write_only=True)
    
    away_team_id = serializers.PrimaryKeyRelatedField(
                    queryset=Team.objects.all(), source='away_team', write_only=True)
    
    league_id = serializers.PrimaryKeyRelatedField(
                    queryset=League.objects.all(), source='league', write_only=True)
    
    season_id = serializers.PrimaryKeyRelatedField(
                    queryset=Season.objects.all(), source='season', write_only=True)
    
    status_id = serializers.PrimaryKeyRelatedField(
                    queryset=Status.objects.all(), source='status', write_only=True)
    
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(), source='hall', write_only=True,
        allow_null=True, required=False
    )

    class Meta:
        model = Match
        fields = '__all__'