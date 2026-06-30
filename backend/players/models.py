from django.db import models
from core.models import Country
from teams.models import Team
from matches.models import Match


class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='player_images/', null=True, blank=True)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='players')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    date_of_birth = models.DateField(null=True, blank=True)
    height_cm = models.IntegerField(null=True, blank=True)
    weight_kg = models.IntegerField(null=True, blank=True)
    wingspan_cm = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class PlayerMatchStatus(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_statuses')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='player_statuses')
    in_game = models.BooleanField(default=False)
    starter = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.player} - match {self.match_id}'


class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='stats')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='player_stats')
    points = models.IntegerField(null=True, blank=True)
    rebounds = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    steals = models.IntegerField(null=True, blank=True)
    blocks = models.IntegerField(null=True, blank=True)
    turnovers = models.IntegerField(null=True, blank=True)
    fouls = models.IntegerField(null=True, blank=True)
    minutes_played = models.IntegerField(null=True, blank=True)
    fg_made = models.IntegerField(null=True, blank=True)
    fg_attempted = models.IntegerField(null=True, blank=True)
    three_pt_made = models.IntegerField(null=True, blank=True)
    three_pt_attempted = models.IntegerField(null=True, blank=True)
    ft_made = models.IntegerField(null=True, blank=True)
    ft_attempted = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.player} - match {self.match_id}'