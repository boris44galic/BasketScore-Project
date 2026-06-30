from rest_framework import serializers
from .models import League, LeagueTeam
from teams.serializers import TeamSerializer
from teams.models import Team
from core.serializers import SeasonSerializer
from core.models import Season


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'


class LeagueTeamSerializer(serializers.ModelSerializer):
    league = LeagueSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    season = SeasonSerializer(read_only=True)

    league_id = serializers.PrimaryKeyRelatedField(
                                    queryset=League.objects.all(), source='league', write_only=True)
    
    team_id = serializers.PrimaryKeyRelatedField(
                                    queryset=Team.objects.all(), source='team', write_only=True)
       
    season_id = serializers.PrimaryKeyRelatedField(
                                    queryset=Season.objects.all(), source='season', write_only=True)
    

    class Meta:
        model = LeagueTeam
        fields = '__all__'