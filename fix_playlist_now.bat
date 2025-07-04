@echo off
chcp 65001 > nul
echo ====================================================
echo       ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С ПЛЕЙЛИСТАМИ
echo ====================================================

cd /d "E:\pravoslavie_portal"

echo Активируем виртуальное окружение...
call .venv\Scripts\activate.bat

echo.
echo Исправляем проблему с плейлистом "борода"...
echo.

python -c "
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Playlist

print('=== ПОИСК ПРОБЛЕМНОГО ПЛЕЙЛИСТА ===')

# Находим все плейлисты
all_playlists = Playlist.objects.all()
print(f'Всего плейлистов: {all_playlists.count()}')

# Показываем все плейлисты
for p in all_playlists:
    print(f'  - ID: {p.id}, Slug: \"{p.slug}\", Title: \"{p.title}\"')

# Ищем проблемный плейлист
problem = Playlist.objects.filter(slug='борода')

if problem.exists():
    print(f'\n🔍 НАЙДЕН ПРОБЛЕМНЫЙ ПЛЕЙЛИСТ:')
    for playlist in problem:
        print(f'  - ID: {playlist.id}')
        print(f'  - Slug: \"{playlist.slug}\"')
        print(f'  - Title: \"{playlist.title}\"')
        print(f'  - Creator: {playlist.creator.username}')
        
        # Изменяем slug
        old_slug = playlist.slug
        new_slug = f'playlist-{playlist.creator.username}-{playlist.id}'
        playlist.slug = new_slug
        playlist.save()
        
        print(f'\n✅ ИСПРАВЛЕНО:')
        print(f'  Старый slug: \"{old_slug}\"')
        print(f'  Новый slug: \"{new_slug}\"')

else:
    print('\n✅ Проблемный плейлист \"борода\" не найден')

print('\n=== ФИНАЛЬНЫЙ СПИСОК ПЛЕЙЛИСТОВ ===')
for p in Playlist.objects.all():
    print(f'  - {p.slug} | {p.title}')

print('\n🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!')
"

echo.
echo ====================================================
echo ГОТОВО! Теперь:
echo 1. Перезагрузите страницу в браузере
echo 2. Попробуйте снова открыть рассказ
echo ====================================================
echo.
pause
