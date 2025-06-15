from django.views.generic import ListView, DetailView

class AudioListView(ListView):
    template_name = 'audio/list.html'
    context_object_name = 'tracks'
    
    def get_queryset(self):
        return []

class AudioDetailView(DetailView):
    template_name = 'audio/detail.html'
    context_object_name = 'track'
    
    def get_object(self):
        return None

class PlaylistListView(ListView):
    template_name = 'audio/playlists.html'
    context_object_name = 'playlists'
    
    def get_queryset(self):
        return []

class PlaylistDetailView(DetailView):
    template_name = 'audio/playlist_detail.html'
    context_object_name = 'playlist'
    
    def get_object(self):
        return None