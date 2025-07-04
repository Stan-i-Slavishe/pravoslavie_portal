#!/usr/bin/env python3
"""
Быстрое исправление функций плейлистов
"""

import re

def fix_views_playlists():
    """Исправляет функции в views_playlists.py"""
    file_path = r'E:\pravoslavie_portal\stories\views_playlists.py'
    
    try:
        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Исправляем функции в views_playlists.py...")
        
        # Заменяем add_to_playlist
        old_add_pattern = r'@login_required\s*@require_http_methods\(\["POST"\]\)\s*def add_to_playlist\(request\):.*?except Exception as e:.*?return JsonResponse\(\{.*?\}\)'
        new_add_function = '''@login_required
@require_http_methods(["POST"])
def add_to_playlist(request):
    """AJAX: Добавление рассказа в плейлист - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    try:
        # Получаем данные из JSON
        if hasattr(request, 'content_type') and request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            # Fallback для form data
            data = request.POST
            
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        print(f"DEBUG: story_id={story_id}, playlist_id={playlist_id}")
        print(f"DEBUG: content_type={getattr(request, 'content_type', 'unknown')}")
        print(f"DEBUG: request.body={request.body}")
        
        if not story_id or not playlist_id:
            return JsonResponse({
                'success': False,
                'message': 'Не указан ID рассказа или плейлиста'
            }, status=400)
        
        story = get_object_or_404(Story, id=story_id)
        playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
        
        # Проверяем, нет ли уже этого рассказа в плейлисте
        if PlaylistItem.objects.filter(playlist=playlist, story=story).exists():
            return JsonResponse({
                'success': False,
                'message': 'Рассказ уже есть в этом плейлисте'
            })
        
        # Определяем порядок (последний + 1)
        last_order = PlaylistItem.objects.filter(
            playlist=playlist
        ).count()
        
        PlaylistItem.objects.create(
            playlist=playlist,
            story=story,
            order=last_order + 1
        )
        
        print(f"DEBUG: Добавлен рассказ {story.title} в плейлист {playlist.title}")
        
        return JsonResponse({
            'success': True,
            'message': f'Рассказ добавлен в плейлист "{playlist.title}"'
        })
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Ошибка в формате данных'
        }, status=400)
    except Exception as e:
        print(f"Add to playlist error: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Произошла ошибка: {str(e)}'
        }, status=500)'''
        
        # Используем более простой подход - заменяем по маркерам
        if 'def add_to_playlist(request):' in content:
            # Находим начало и конец функции
            lines = content.split('\n')
            new_lines = []
            in_add_function = False
            indent_level = 0
            
            for line in lines:
                if 'def add_to_playlist(request):' in line:
                    in_add_function = True
                    indent_level = len(line) - len(line.lstrip())
                    # Добавляем новую функцию
                    new_lines.extend(new_add_function.split('\n'))
                    continue
                elif in_add_function:
                    # Проверяем, закончилась ли функция
                    current_indent = len(line) - len(line.lstrip()) if line.strip() else indent_level + 1
                    if line.strip() and current_indent <= indent_level and (line.startswith('def ') or line.startswith('class ') or line.startswith('@')):
                        in_add_function = False
                        new_lines.append(line)
                    # Пропускаем строки старой функции
                    continue
                else:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
        
        # Сохраняем файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Функция add_to_playlist исправлена!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при исправлении: {e}")
        return False

def fix_story_detail_js():
    """Исправляет JavaScript в story_detail.html"""
    file_path = r'E:\pravoslavie_portal\templates\stories\story_detail.html'
    
    try:
        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Исправляем JavaScript в story_detail.html...")
        
        # Заменяем функцию togglePlaylistStory
        old_toggle_pattern = r'function togglePlaylistStory\(playlistId, storyId, checkbox\) \{.*?\}\s*(?=\n\s*//|function|</script>)'
        
        new_toggle_function = '''function togglePlaylistStory(playlistId, storyId, checkbox) {
    console.log('togglePlaylistStory called:', { playlistId, storyId, checked: checkbox.checked });
    
    const isAdding = checkbox.checked;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // ИСПРАВЛЕНИЕ: Используем правильные URL из urls.py
    const url = isAdding ? '/stories/playlist/add-story/' : '/stories/playlist/remove-story/';
    
    const requestData = {
        playlist_id: playlistId,
        story_id: storyId
    };
    
    console.log('Отправляем запрос:', url, requestData);
    
    // Блокируем checkbox на время запроса
    checkbox.disabled = true;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        // Проверяем тип контента
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Сервер вернул не JSON ответ');
        }
        
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        
        if (data.success) {
            showToast(data.message, 'success');
        } else {
            // Откатываем состояние checkbox
            checkbox.checked = !checkbox.checked;
            showToast(data.message || 'Ошибка при обновлении плейлиста', 'error');
        }
    })
    .catch(error => {
        console.error('Playlist error:', error);
        
        // Откатываем состояние checkbox
        checkbox.checked = !checkbox.checked;
        showToast('Произошла ошибка при обновлении плейлиста: ' + error.message, 'error');
    })
    .finally(() => {
        // Разблокируем checkbox
        checkbox.disabled = false;
    });
}'''
        
        # Простая замена
        if 'function togglePlaylistStory(' in content:
            # Найдем начало функции
            start_pattern = 'function togglePlaylistStory(playlistId, storyId, checkbox) {'
            start_idx = content.find(start_pattern)
            
            if start_idx != -1:
                # Найдем конец функции (следующую функцию или </script>)
                brace_count = 0
                end_idx = start_idx
                in_function = False
                
                for i, char in enumerate(content[start_idx:], start_idx):
                    if char == '{':
                        brace_count += 1
                        in_function = True
                    elif char == '}':
                        brace_count -= 1
                        if in_function and brace_count == 0:
                            end_idx = i + 1
                            break
                
                # Заменяем функцию
                content = content[:start_idx] + new_toggle_function + content[end_idx:]
        
        # Сохраняем файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ JavaScript в story_detail.html исправлен!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при исправлении JavaScript: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Быстрое исправление плейлистов")
    print("=" * 40)
    
    # Исправляем Python функции
    if fix_views_playlists():
        print("✅ Python функции исправлены")
    else:
        print("❌ Ошибка при исправлении Python функций")
    
    # Исправляем JavaScript
    if fix_story_detail_js():
        print("✅ JavaScript исправлен")
    else:
        print("❌ Ошибка при исправлении JavaScript")
    
    print("\n🎯 Что делать дальше:")
    print("1. Перезапустите Django сервер")
    print("2. Откройте страницу рассказа")
    print("3. Откройте консоль браузера (F12)")
    print("4. Попробуйте добавить рассказ в плейлист")
    print("5. Проверьте DEBUG сообщения в консоли Django и браузера")
