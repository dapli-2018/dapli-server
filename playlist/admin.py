from django.contrib import admin
from .models import SongInfo, Playlist

# Register your models here.
admin.site.register(SongInfo)
admin.site.register(Playlist)
