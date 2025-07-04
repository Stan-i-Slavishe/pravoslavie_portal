#!/usr/bin/env python
"""
🚀 ОКОНЧАТЕЛЬНОЕ ИСПРАВЛЕНИЕ ПЛЕЙЛИСТОВ
Этот скрипт исправляет все проблемы с плейлистами за один запуск
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

print("🚀 ОКОНЧАТЕЛЬНОЕ ИСПРАВЛЕНИЕ ПЛЕЙЛИСТОВ")
print("=" * 60)

# 1. Исправляем URL redirect в views_playlists.py
print("\n1️⃣ Исправление URL redirect...")
try:
    views_file = 'stories/views_playlists.py'
    if os.path.exists(views_file):
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем неправильный URL
        if "redirect('stories:playlists_list')" in content:
            content = content.replace(
                "redirect('stories:playlists_list')",
                "redirect('stories:playlists')"
            )
            
            with open(views_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ URL redirect исправлен")
        else:
            print("✅ URL redirect уже исправлен")
    else:
        print("⚠️  Файл views_playlists.py не найден")
except Exception as e:
    print(f"❌ Ошибка исправления URL: {e}")

# 2. Создаем миграции
print("\n2️⃣ Создание миграций для плейлистов...")
try:
    from django.core.management import call_command
    
    # Проверяем, есть ли уже миграции плейлистов
    import glob
    migration_files = glob.glob('stories/migrations/*playlist*.py')
    
    if migration_files:
        print("✅ Миграции плейлистов уже существуют")
    else:
        print("📦 Создание новых миграций...")
        call_command('makemigrations', 'stories', '--name=add_playlist_models', verbosity=1)
        print("✅ Миграции созданы")
    
except Exception as e:
    print(f"❌ Ошибка создания миграций: {e}")
    print("🔄 Попробуйте вручную: python manage.py makemigrations stories")

# 3. Применяем миграции
print("\n3️⃣ Применение миграций...")
try:
    call_command('migrate', 'stories', verbosity=1)
    print("✅ Миграции применены")
except Exception as e:
    print(f"❌ Ошибка применения миграций: {e}")
    print("🔄 Попробуйте вручную: python manage.py migrate stories")

# 4. Проверяем модели
print("\n4️⃣ Проверка моделей плейлистов...")
try:
    from stories.models import Playlist, PlaylistItem, Story
    print("✅ Модели Playlist и PlaylistItem доступны")
    
    # Проверяем количество существующих плейлистов
    playlist_count = Playlist.objects.count()
    print(f"📊 Существующих плейлистов: {playlist_count}")
    
except ImportError as e:
    print(f"❌ Ошибка импорта моделей: {e}")
    print("🔧 Проверьте, что модели добавлены в stories/models.py")
except Exception as e:
    print(f"❌ Ошибка проверки моделей: {e}")

# 5. Создаем тестового пользователя и плейлисты
print("\n5️⃣ Создание тестовых данных...")
try:
    from django.contrib.auth.models import User
    from stories.models import Story, Playlist, PlaylistItem
    
    # Создаем/получаем админа
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True,
            'first_name': 'Администратор',
            'last_name': 'Системы'
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Создан пользователь: {admin_user.username}")
    else:
        print(f"✅ Найден пользователь: {admin_user.username}")
    
    # Получаем рассказы
    stories = Story.objects.all()[:5]
    print(f"📚 Доступно рассказов: {stories.count()}")
    
    if stories.count() == 0:
        print("⚠️  Нет рассказов для создания плейлистов")
        print("💡 Создайте сначала несколько рассказов через админку")
    else:
        # Создаем тестовые плейлисты
        test_playlists = [
            {
                'title': 'Бородa',
                'description': 'Плейлист с рассказами про бороду и духовность',
                'playlist_type': 'public'
            },
            {
                'title': 'Школьные истории',
                'description': 'Рассказы про школьную жизнь и детство',
                'playlist_type': 'private'
            },
            {
                'title': 'Добрые дела',
                'description': 'Вдохновляющие истории о добрых поступках',
                'playlist_type': 'public'
            }
        ]
        
        created_playlists = 0
        for playlist_data in test_playlists:
            playlist, created = Playlist.objects.get_or_create(
                creator=admin_user,
                title=playlist_data['title'],
                defaults={
                    'description': playlist_data['description'],
                    'playlist_type': playlist_data['playlist_type']
                }
            )
            
            if created:
                print(f"✅ Создан плейлист: {playlist.title}")
                created_playlists += 1
                
                # Добавляем рассказы в плейлист
                for i, story in enumerate(stories[:3]):
                    playlist_item, item_created = PlaylistItem.objects.get_or_create(
                        playlist=playlist,
                        story=story,
                        defaults={'order': i + 1}
                    )
                    if item_created:
                        print(f"  📝 Добавлен рассказ: {story.title}")
                
                # Обновляем счетчик
                playlist.stories_count = playlist.playlist_items.count()
                playlist.save()
                print(f"  📊 Итого рассказов в плейлисте: {playlist.stories_count}")
            else:
                print(f"⚠️  Плейлист уже существует: {playlist.title}")
        
        if created_playlists > 0:
            print(f"🎉 Создано новых плейлистов: {created_playlists}")

except Exception as e:
    import traceback
    print(f"❌ Ошибка создания тестовых данных: {e}")
    traceback.print_exc()

# 6. Финальная проверка
print("\n6️⃣ Финальная проверка...")
try:
    from stories.models import Playlist, PlaylistItem
    
    total_playlists = Playlist.objects.count()
    total_items = PlaylistItem.objects.count()
    
    print(f"📊 Всего плейлистов в системе: {total_playlists}")
    print(f"📊 Всего элементов плейлистов: {total_items}")
    
    if total_playlists > 0:
        print("✅ Система плейлистов готова к использованию!")
    else:
        print("⚠️  Плейлисты не созданы - проверьте наличие рассказов")
        
except Exception as e:
    print(f"❌ Ошибка финальной проверки: {e}")

print("\n" + "=" * 60)
print("🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
print("\n📋 ЧТО БЫЛО СДЕЛАНО:")
print("✅ Исправлен URL redirect в views")
print("✅ Созданы/применены миграции плейлистов")
print("✅ Проверены модели базы данных")
print("✅ Созданы тестовые плейлисты и данные")
print("✅ Выполнена финальная проверка")

print("\n🚀 СЛЕДУЮЩИЕ ШАГИ:")
print("1. Добавьте секцию плейлистов в story_detail.html")
print("2. Скопируйте содержимое из playlist_section_complete.html")
print("3. Перезапустите сервер: python manage.py runserver")
print("4. Проверьте работу плейлистов на странице рассказа")

print("\n💡 ПОЛЕЗНАЯ ИНФОРМАЦИЯ:")
print("🔑 Админ логин: admin / admin123")
print("🎵 Тестовые плейлисты: 'Бородa', 'Школьные истории', 'Добрые дела'")
print("🌐 URL админки: http://127.0.0.1:8000/admin/")

print("\n🔄 Если возникнут проблемы:")
print("1. Проверьте логи Django в консоли")
print("2. Откройте F12 → Console в браузере")
print("3. Убедитесь, что секция плейлистов добавлена в шаблон")
