from django.views.generic import ListView, DetailView

class AudioListView(ListView):
    template_name = 'audio/audio_list.html'
    context_object_name = 'audio_list'
    
    def get_queryset(self):
        # Демо-данные для аудио
        return [
            {
                'id': 1,
                'title': 'Акафист Божией Матери',
                'author': 'Церковный хор',
                'duration': '45:30',
                'file_url': '#'
            },
            {
                'id': 2,
                'title': 'О молитве и посте',
                'author': 'Протоиерей Александр',
                'duration': '28:15',
                'file_url': '#'
            },
            {
                'id': 3,
                'title': 'Житие святого Серафима',
                'author': 'Чтец Михаил',
                'duration': '1:12:45',
                'file_url': '#'
            }
        ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Аудио'
        return context

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Плейлисты'
        return context

class PlaylistDetailView(DetailView):
    template_name = 'audio/playlist_detail.html'
    context_object_name = 'playlist'
    
    def get_object(self):
        return None