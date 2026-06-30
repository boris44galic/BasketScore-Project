from django.db import models
from teams.models import Team
from leagues.models import League
from core.models import Season, Hall


class Status(models.Model):
    name = models.CharField(max_length = 50) # live, odlozene, odigrane

    def __str__(self):
        return self.name


class Match(models.Model):

    home_team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = 'home_matches')
    away_team = models.ForeignKey(Team, on_delete =models.CASCADE, related_name = 'away_matches')
    league = models.ForeignKey(League, on_delete = models.CASCADE, related_name = 'matches')
    season = models.ForeignKey(Season, on_delete = models.CASCADE, related_name = 'matches')
    status = models.ForeignKey(Status, on_delete = models.CASCADE, related_name ='matches')
    hall = models.ForeignKey(Hall, on_delete = models.SET_NULL, null=True, blank=True, related_name='matches')
    match_date = models.DateTimeField()
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-match_date']

    def __str__(self):
        return f'{self.home_team} vs {self.away_team} ({self.match_date.date()})'
