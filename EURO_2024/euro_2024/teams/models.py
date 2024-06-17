from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    team = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='teams/images')
    url = models.URLField(blank=True)
    group = models.CharField(max_length=10, null=True, blank=True)
    squad = models.TextField(null=True, blank=True)
    qualifying = models.CharField(max_length=100, null=True, blank=True)
    euro_best = models.CharField(max_length=100, null=True, blank=True)
    coach = models.CharField(max_length=30)
    key_player = models.CharField(max_length=30, null=True, blank=True)
    did_you_know = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.team
    

    class Meta:
        ordering = ['team']