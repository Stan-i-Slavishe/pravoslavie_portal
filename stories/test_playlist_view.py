from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stories.models import Playlist

@login_required
def playlist_management_test(request):
    """Тестовая страница управления плейлистами"""
    playlists = Playlist.objects.filter(creator=request.user)
    
    context = {
        'playlists': playlists
    }
    
    return render(request, 'stories/playlist_management_test.html', context)
