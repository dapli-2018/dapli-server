from rest_framework import serializers
from .models import Playlist, SongInfo

class PlaylistFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('title', 'author', 'date', 'content', 'tag')

class PlaylistImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('profile_image')

class SongInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongInfo
        fields = ('title', 'artist', 'album', 'is_on_playlist', 'is_played')
