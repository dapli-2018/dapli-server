import json
from random import randint
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from playlist.models import SongInfo, Playlist

class HostView(APIView):
    def post(self, request):
        songs = request.data.get('songs')

        if type(songs) is not list:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        if Playlist.objects.count() < 9000:
            for i in range(1000, 9999):
                try:
                    key = randint(1000, 9999)
                    g = Playlist.objects.create(key=key)
                    g.save()
                except IntegrityError:
                    continue
                else:
                    break
        else:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        for i in range(len(songs)):
            songinfo = SongInfo.objects.create(
                playlist=g,
                index=i,
                title=songs[i][0],
                artist=songs[i][1],
                album=songs[i][2],
            )
            songinfo.save()

        return JsonResponse({'key': key}, status=status.HTTP_201_CREATED)

    def get(self, request):
        key = request.GET.get('key')
        try:
            g = Playlist.objects.get(key=key)
        except Playlist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)


        songs = list(SongInfo.objects.filter(playlist=g).order_by('index')\
            .values_list('title', 'is_on_playlist', 'is_played'))
        return JsonResponse({'songs': songs}, status=status.HTTP_200_OK)

    def delete(self, request):
        key = request.data.get('key')
        try:
            g = Playlist.objects.get(key=key)
            g.delete()
        except Playlist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        return JsonResponse({}, status=status.HTTP_200_OK)


class GuestView(APIView):
    def get(self, request):
        key = request.GET.get('key')

        try:
            p = Playlist.objects.get(key=key)
        except Playlist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        songs = SongInfo.objects.filter(playlist=p).order_by('index') \
            .values_list('title', 'artist', 'album', 'is_on_playlist', 'is_played')
        return JsonResponse({'songs': list(songs), 'id': p.id}, status=status.HTTP_200_OK)

    def put(self, request):
        id = request.data.get('id')
        new_playlist = request.data.get('songs')

        try:
            p = Playlist.objects.get(id=id)
        except Playlist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        if type(new_playlist) is not list:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        with transaction.atomic():
            for song in SongInfo.objects.filter(playlist=p):
                for i in range(len(new_playlist)):
                    if song.title == new_playlist[i][0] :
                        song.index = i
                        song.is_on_playlist = new_playlist[i][3]
                        song.is_played = new_playlist[i][4]
                        song.save()

        return JsonResponse({}, status=status.HTTP_200_OK)










