from django.db import models
from core.models import City


class Team(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name
