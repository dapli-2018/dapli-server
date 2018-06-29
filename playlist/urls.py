from django.urls import path
from playlist import views

urlpatterns = [
    path('host', views.HostView.as_view()),
    path('guest', views.GuestView.as_view()),
    path('image', views.ImageView.as_view()),
    path('keygen', views.KeyView.as_view()),
    path('playlist', views.playlist_detail),
    path('newsfeed', views.newsfeed),
    path('search', views.search)
]
