from django.urls import path
from playlist import views

urlpatterns = [
    path('host', views.HostView.as_view())
]
