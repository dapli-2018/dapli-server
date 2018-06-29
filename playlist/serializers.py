from rest_framework import serializers
from .models import Playlist, SongInfo, Like

class PlaylistFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'title', 'author', 'date', 'content', 'tag')

class PlaylistImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('image',)

class SongInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongInfo
        fields = ('title', 'artist', 'album', 'is_on_playlist', 'is_played')

class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ('count',)
