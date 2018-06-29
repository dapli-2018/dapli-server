from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator)

# Create your models here.

class GroupPlaylist(models.Model):
    # 4자리수 key
    key = models.IntegerField(unique=True, validators=[MaxValueValidator(9999), MinValueValidator(1000)])
    # JSON list; view에서는 JSON파싱해서 사용

class SongInfo(models.Model):
    group_playlist = models.ForeignKey(GroupPlaylist, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    title = models.TextField(default="NoTitle")
    artist = models.TextField(default="")
    album = models.TextField(default="")
    is_on_playlist = models.BooleanField(default=True)
    is_played = models.BooleanField(default=False)
