from django.db import models
from teams.models import Team
from core.models import Season


class League(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='league_logos/', null=True, blank=True)

    def __str__(self):
        return self.name


class LeagueTeam(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league_teams')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='league_teams')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='league_teams')

    win = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)

    class Meta:
        unique_together = ('league', 'team', 'season')

    def __str__(self):
        return f'{self.team} in {self.league} ({self.season} season)'
