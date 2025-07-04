@echo off
echo ====================================================
echo ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С ПЛЕЙЛИСТАМИ
echo ====================================================

cd /d "E:\pravoslavie_portal"

echo Активируем виртуальное окружение...
call .venv\Scripts\activate.bat

echo.
echo Запускаем исправление плейлистов...
python manage.py fix_playlists

echo.
echo Если команды нет, запускаем альтернативный скрипт...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Playlist
from django.db import transaction

print('=== ИСПРАВЛЕНИЕ ПЛЕЙЛИСТОВ ===')

with transaction.atomic():
    # Находим проблемный плейлист
    problematic = Playlist.objects.filter(slug='борода')
    
    if problematic.exists():
        for playlist in problematic:
            old_slug = playlist.slug
            new_slug = f'playlist-{playlist.creator.username}-{playlist.id}'
            playlist.slug = new_slug
            playlist.save()
            print(f'✅ Изменен slug: {old_slug} -> {new_slug}')
    else:
        print('✅ Проблемный плейлист не найден')
    
    # Показываем все плейлисты
    print('\n📊 ТЕКУЩИЕ ПЛЕЙЛИСТЫ:')
    for p in Playlist.objects.all():
        print(f'   - {p.slug} | {p.title} | {p.creator.username}')

print('\n🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!')
"

echo.
echo ====================================================
echo ГОТОВО! Теперь перезагрузите страницу в браузере
echo ====================================================
pause
