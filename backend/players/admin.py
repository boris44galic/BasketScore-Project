from django.contrib import admin
from .models import Player, PlayerStats, PlayerMatchStatus, Position

admin.site.register(Position)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team', 'position', 'nationality')
    list_filter = ('team', 'position', 'nationality')
    search_fields = ('first_name', 'last_name')


@admin.register(PlayerMatchStatus)
class PlayerMatchStatusAdmin(admin.ModelAdmin):
    list_display = ('player', 'match', 'in_game', 'starter')
    list_filter = ('in_game', 'starter')
    search_fields = ('player__first_name', 'player__last_name')


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'match', 'points', 'rebounds', 'assists', 'minutes_played')
    list_filter = ('match__league', 'match__season')
    search_fields = ('player__first_name', 'player__last_name')
