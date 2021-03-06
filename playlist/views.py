from random import randint
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SongInfo, Playlist, AuthKey, Like
from .serializers import SongInfoSerializer, PlaylistFeedSerializer, PlaylistImageSerializer, LikeSerializer

class HostView(APIView):
    def post(self, request):
        songs = request.data.get('songs')
        title = request.data.get('title')
        author = request.data.get('author')
        content = request.data.get('content')
        tag = request.data.get('tag')

        if type(songs) is not list or title == None:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        p = Playlist.objects.create(title=title, author=author, content=content, tag=tag)
        Like.objects.create(playlist=p).save()

        for i in range(len(songs)):
            songinfo = SongInfo.objects.create(
                playlist=p,
                index=i,
                title=songs[i][0],
                artist=songs[i][1],
                album=songs[i][2],
            )
            songinfo.save()

        return JsonResponse({'id': p.id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        id = request.GET.get('id')
        try:
            p = Playlist.objects.get(id=id)
        except Playlist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        songs = list(SongInfo.objects.filter(playlist=p).order_by('index')\
            .values_list('title', 'is_on_playlist', 'is_played'))
        return JsonResponse({'songs': songs}, status=status.HTTP_200_OK)

    def delete(self, request):
        id = request.data.get('id')
        try:
            p = Playlist.objects.get(id=id)
            p.delete()
        except Playlist.DoesNotExist:
            pass
        return JsonResponse({}, status=status.HTTP_200_OK)

class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request):
        id = request.GET.get('id')
        image_serializer = PlaylistImageSerializer(Playlist.objects.get(id=id))
        return Response(image_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        id = request.data.get('id')
        image_serializer = PlaylistImageSerializer(Playlist.objects.get(id=id), data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KeyView(APIView):
    def get(self, request):
        id = request.data.get('id')

        try:
            p = Playlist.objects.get(id=id)
        except Playlist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        try:
            k = AuthKey.objects.get(playlist=p)
        except AuthKey.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({'key': k.key}, status=status.HTTP_200_OK)

    def post(self, request):
        id = request.data.get('id')

        try:
            p = Playlist.objects.get(id=id)
        except Playlist.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

        if AuthKey.objects.count() < 9000:
            for i in range(1000, 9999):
                try:
                    key = randint(1000, 9999)
                    k = AuthKey.objects.create(key=key, playlist=p)
                    k.save()
                except IntegrityError:
                    continue
                else:
                    return JsonResponse({'key': key}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def delete(self, request):
        key = request.data.get('key')
        AuthKey.objects.get(key=key).delete()
        return JsonResponse({}, status=status.HTTP_200_OK)


class GuestView(APIView):
    def get(self, request):
        key = request.GET.get('key')

        try:
            k = AuthKey.objects.get(key=key)
            p = Playlist.objects.get(authkey=k)
        except AuthKey.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)
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

@api_view(['GET'])
def playlist_detail(request):
    id = request.GET.get('id')
    try:
        p = Playlist.objects.get(id=id)
    except Playlist.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_412_PRECONDITION_FAILED)

    s = SongInfo.objects.filter(playlist=p).order_by('index')
    serializer = SongInfoSerializer(s, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def newsfeed(request):
    serializer = PlaylistFeedSerializer(Playlist.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search(request):
    criterion = request.GET.get('criterion')
    query = request.GET.get('query')

    if (criterion == "title"):
        ps = Playlist.objects.filter(title__icontains=query)
        result_serializer = PlaylistFeedSerializer(ps, many=True)
        return Response(result_serializer.data, status.HTTP_200_OK)

    elif (criterion == "author"):
        ps = Playlist.objects.filter(author__icontains=query)
        result_serializer = PlaylistFeedSerializer(ps, many=True)
        return Response(result_serializer, status=status.HTTP_200_OK)

class LikeView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        p = Playlist.objects.get(id=id)
        like_serializer = LikeSerializer(p)
        return Response(like_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        id = request.GET.get('id')
        p = Playlist.objects.get(id=id)
        l = Like.objects.get(playlist=p)
        l.count += 1
        return JsonResponse({'count': l.count}, status=status.HTTP_200_OK)


