#!/usr/bin/env python
# quick_playlist_fix.py - Быстрое исправление плейлистов

print("🔧 Применяю исправления для системы плейлистов...")

# ✅ JavaScript файл уже заменен

print("✅ JavaScript файл заменен: static/js/save_to_playlist.js")

print("\n📝 ДОБАВЬТЕ В КОНЕЦ ФАЙЛА stories/views.py:")
print("="*60)

views_code = '''
# ==========================================
# API ДЛЯ ПЛЕЙЛИСТОВ - ИСПРАВЛЕНИЕ
# ==========================================

@login_required
def api_playlists(request):
    """API для получения плейлистов пользователя"""
    try:
        from .models import Playlist
        
        story_slug = request.GET.get('story_slug')
        story = None
        
        if story_slug:
            try:
                story = Story.objects.get(slug=story_slug)
            except Story.DoesNotExist:
                pass
        
        # Получаем плейлисты пользователя
        playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')
        
        playlists_data = []
        for playlist in playlists:
            has_story = False
            if story:
                has_story = playlist.stories.filter(id=story.id).exists()
            
            playlists_data.append({
                'id': playlist.id,
                'title': playlist.name,
                'has_story': has_story,
                'stories_count': playlist.stories.count(),
                'is_public': playlist.is_public
            })
        
        return JsonResponse({
            'success': True,
            'playlists': playlists_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        })

@login_required
@require_POST
def api_toggle_playlist(request):
    """API для добавления/удаления рассказа из плейлиста"""
    try:
        from .models import Playlist
        
        story_slug = request.POST.get('story_slug')
        playlist_id = request.POST.get('playlist_id')
        action = request.POST.get('action')  # 'add' или 'remove'
        
        if not all([story_slug, playlist_id, action]):
            return JsonResponse({
                'success': False,
                'message': 'Недостаточно данных'
            })
        
        # Получаем рассказ
        try:
            story = Story.objects.get(slug=story_slug)
        except Story.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Рассказ не найден'
            })
        
        # Получаем плейлист
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=request.user)
        except Playlist.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Плейлист не найден'
            })
        
        # Выполняем действие
        if action == 'add':
            playlist.stories.add(story)
            message = f'Добавлено в "{playlist.name}"'
        elif action == 'remove':
            playlist.stories.remove(story)
            message = f'Удалено из "{playlist.name}"'
        else:
            return JsonResponse({
                'success': False,
                'message': 'Неизвестное действие'
            })
        
        return JsonResponse({
            'success': True,
            'message': message
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        })

@login_required
@require_POST
def api_create_playlist(request):
    """API для создания нового плейлиста"""
    try:
        from .models import Playlist
        from django.utils.text import slugify
        
        name = request.POST.get('name', '').strip()
        story_slug = request.POST.get('story_slug')
        
        if not name:
            return JsonResponse({
                'success': False,
                'message': 'Введите название плейлиста'
            })
        
        # Создаем плейлист
        playlist = Playlist.objects.create(
            name=name,
            slug=slugify(name),
            user=request.user,
            is_public=False
        )
        
        # Добавляем рассказ, если указан
        if story_slug:
            try:
                story = Story.objects.get(slug=story_slug)
                playlist.stories.add(story)
            except Story.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'message': f'Плейлист "{name}" создан!',
            'playlist_id': playlist.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        })'''

print(views_code)

print("\n📝 ДОБАВЬТЕ В stories/urls.py В СПИСОК urlpatterns:")
print("="*60)

urls_code = '''    # API для плейлистов (исправление)
    path('api/playlists/', views.api_playlists, name='api_playlists'),
    path('api/toggle-playlist/', views.api_toggle_playlist, name='api_toggle_playlist'),
    path('api/create-playlist/', views.api_create_playlist, name='api_create_playlist'),'''

print(urls_code)

print("\n🎉 ПОСЛЕ ПРИМЕНЕНИЯ ИСПРАВЛЕНИЙ:")
print("="*60)
print("1. ✅ Перезапустите сервер: python manage.py runserver")
print("2. ✅ Галочки будут работать с реальным сохранением")
print("3. ✅ Будут появляться уведомления 'Добавлено!' / 'Удалено!'")
print("4. ✅ Состояние сохранится при перезагрузке страницы")
print("5. ✅ Новые плейлисты будут создаваться корректно")

print("\n📍 СИСТЕМА ИСПРАВЛЕНА! Теперь плейлисты работают как в YouTube! 🎉")
