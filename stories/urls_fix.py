# Добавьте эти URL-ы в stories/urls.py после существующих

# API для плейлистов (исправление)
path('api/playlists/', views.api_playlists, name='api_playlists'),
path('api/toggle-playlist/', views.api_toggle_playlist, name='api_toggle_playlist'),
path('api/create-playlist/', views.api_create_playlist, name='api_create_playlist'),
