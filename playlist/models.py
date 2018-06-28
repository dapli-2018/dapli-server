from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator)

# Create your models here.

class GroupPlaylist(models.Model):
    # 4자리수 key
    key = models.IntegerField(unique=True, validators=[MaxValueValidator(9999), MinValueValidator(1000)])
    # JSON list; view에서는 JSON파싱해서 사용
    indices = models.TextField(null=False, blank=False)

class SongInfo(models.Model):
    key = models.ForeignKey(GroupPlaylist, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    title = models.TextField(default="NoTitle")
    Artist = models.TextField(default="")
    Album = models.TextField(default="")
