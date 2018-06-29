from django.contrib import admin
from .models import SongInfo, Playlist, AuthKey

# Register your models here.
admin.site.register(SongInfo)
admin.site.register(Playlist)
admin.site.register(AuthKey)
