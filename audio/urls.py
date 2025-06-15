from django.urls import path
from . import views

app_name = 'audio'

urlpatterns = [
    path('', views.AudioListView.as_view(), name='list'),
    path('<slug:slug>/', views.AudioDetailView.as_view(), name='detail'),
    path('playlists/', views.PlaylistListView.as_view(), name='playlists'),
    path('playlists/<slug:slug>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
]