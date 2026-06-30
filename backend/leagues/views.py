from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import League, LeagueTeam
from .serializers import LeagueSerializer, LeagueTeamSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class LeagueTeamViewSet(viewsets.ModelViewSet):
    queryset = LeagueTeam.objects.select_related('league', 'team', 'season').all()
    serializer_class = LeagueTeamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['league', 'season']
