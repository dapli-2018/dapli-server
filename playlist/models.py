from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator)

# Create your models here.

class Playlist(models.Model):
    key = models.IntegerField(unique=True, validators=[MaxValueValidator(9999), MinValueValidator(1000)])
    title = models.CharField(max_length=90)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=300)


class SongInfo(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    title = models.CharField(default="NoTitle", max_length=90)
    artist = models.TextField(default="", max_length=90)
    album = models.TextField(default="", max_length=90)
    is_on_playlist = models.BooleanField(default=True)
    is_played = models.BooleanField(default=False)
