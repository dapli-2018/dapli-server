import json
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from playlist.models import SongInfo, GroupPlaylist


class HostView(APIView):
    def post(self, request):
        songs = request.data.get('songs')

        if type(songs) is not list:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        max_key = GroupPlaylist.objects.order_by('-key').first()
        indices = json.dumps(list(range(len(songs))))
        if max_key == None:
            key = 1000
            g = GroupPlaylist.objects.create(key=key)
            g.save()
        else:
            try:
                g = GroupPlaylist.objects.create(key=max_key.key + 1)
                g.save()
                key = g.key
            except ValidationError:  # key를 9999까지 발급했을 때
                try:
                    g = GroupPlaylist.objects.create(key=1000)
                    g.save()
                except IntegrityError:  # 너무 많은 접속자로 잠시 제한
                    return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        for i in range(len(songs)):
            songinfo = SongInfo.objects.create(
                group_playlist=g,
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
            g = GroupPlaylist.objects.get(key=key)
        except GroupPlaylist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)


        songs = list(SongInfo.objects.filter(group_playlist=g).order_by('index')\
            .values_list('title', 'is_on_playlist', 'is_played'))
        return JsonResponse({'songs': songs}, status=status.HTTP_200_OK)

    def delete(self, request):
        key = request.data.get('key')
        try:
            g = GroupPlaylist.objects.get(key=key)
            g.delete()
        except GroupPlaylist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        return JsonResponse({}, status=status.HTTP_200_OK)


class GuestView(APIView):
    def get(self, request):
        key = request.GET.get('key')

        try:
            g = GroupPlaylist.objects.get(key=key)
        except GroupPlaylist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        songs = SongInfo.objects.filter(group_playlist=g).order_by('index') \
            .values_list('title', 'artist', 'album', 'is_on_playlist', 'is_played')
        return JsonResponse({'songs': list(songs)}, status=status.HTTP_200_OK)

    def put(self, request):
        key = request.data.get('key')
        new_playlist = request.data.get('songs')

        try:
            g = GroupPlaylist.objects.get(key=key)
        except GroupPlaylist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        if type(new_playlist) is not list:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        with transaction.atomic():
            for song in SongInfo.objects.filter(group_playlist=g):
                for i in range(len(new_playlist)):
                    if (song.title == new_playlist[i][0]):
                        song.index = i
                        song.is_on_playlist = new_playlist[i][3]
                        song.is_played = new_playlist[i][4]
                        song.save()

        return JsonResponse({}, status=status.HTTP_200_OK)










