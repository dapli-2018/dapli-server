import json
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from playlist.models import SongInfo, GroupPlaylist


class HostView(APIView):
    def post(self, request):
        songs = request.POST.get('songs')
        if type(songs) is not list:
            return JsonResponse({'code': status.HTTP_412_PRECONDITION_FAILED})

        key = GroupPlaylist.objects.order_by('key').first()
        indices = json.dumps(list(range(len(songs))))
        if key == None:
            key = 1000
            g = GroupPlaylist.objects.create(key=key, indices=str(indices))
            g.save()
        else:
            try:
                g = GroupPlaylist.objects.create(key=key + 1, indices=str(indices))
                g.save()
            except ValidationError:  # key를 9999까지 발급했을 때
                try:
                    g = GroupPlaylist.objects.create(key=1000, indices=str(indices))
                    g.save()
                except IntegrityError:  # 너무 많은 접속자로 잠시 제한
                    return JsonResponse({'code': status.HTTP_503_SERVICE_UNAVAILABLE})

        for i in range(songs):
            songinfo = SongInfo.objects.create(
                key=g,
                index=i,
                title=songs[i][0],
                artist=songs[i][1],
                album=songs[i][2]
            )
            songinfo.save()

        return JsonResponse({'code': status.HTTP_201_CREATED, 'key': key})





