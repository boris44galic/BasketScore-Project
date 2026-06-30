from rest_framework import viewsets, filters
from .models import Match, Status
from .serializers import MatchSerializer, StatusSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related(
        'home_team', 'away_team', 'league', 'season', 'status', 'hall'
    ).all()
    serializer_class = MatchSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['match_date']

    def get_queryset(self):
        qs = super().get_queryset()
        
        league_id = self.request.query_params.get('league')
        season_id = self.request.query_params.get('season')
        status_id = self.request.query_params.get('status')
        team_id = self.request.query_params.get('team')

        if league_id:
            qs = qs.filter(league_id=league_id)
        if season_id:
            qs = qs.filter(season_id=season_id)
        if status_id:
            qs = qs.filter(status_id=status_id)
        if team_id:
            qs = qs.filter(home_team_id=team_id) | qs.filter(away_team_id=team_id)
        return qs