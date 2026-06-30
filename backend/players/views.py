from rest_framework import viewsets, filters
from .models import Player, PlayerStats, PlayerMatchStatus, Position
from .serializers import PlayerSerializer, PlayerStatsSerializer, PlayerMatchStatusSerializer, PositionSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.select_related('nationality', 'team', 'position').all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = super().get_queryset()
        team_id = self.request.query_params.get('team')
        position_id = self.request.query_params.get('position')
        if team_id:
            qs = qs.filter(team_id=team_id)
        if position_id:
            qs = qs.filter(position_id=position_id)
        return qs


class PlayerMatchStatusViewSet(viewsets.ModelViewSet):
    queryset = PlayerMatchStatus.objects.select_related(
        'player', 'player__team', 'player__team__city',
        'player__nationality', 'player__position', 'match',
    ).all()
    serializer_class = PlayerMatchStatusSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        player_id = self.request.query_params.get('player')
        match_id = self.request.query_params.get('match')
        if player_id:
            qs = qs.filter(player_id=player_id)
        if match_id:
            qs = qs.filter(match_id=match_id)
        return qs


class PlayerStatsViewSet(viewsets.ModelViewSet):
    queryset = PlayerStats.objects.select_related(
        'player', 'player__team', 'player__team__city',
        'player__nationality', 'player__position', 'match',
    ).all()
    serializer_class = PlayerStatsSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        player_id = self.request.query_params.get('player')
        match_id = self.request.query_params.get('match')
        if player_id:
            qs = qs.filter(player_id=player_id)
        if match_id:
            qs = qs.filter(match_id=match_id)
        return qs