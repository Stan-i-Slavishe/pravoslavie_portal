@echo off
echo 🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С ДЕТАЛИЗАЦИЕЙ РАССКАЗОВ
echo.

echo ===============================================
echo 📋 ШАГ 1: Диагностика ссылок в списке
echo ===============================================

python manage.py shell -c "
from django.urls import reverse
from stories.models import Story

print('=== ПРОВЕРКА URL ДЛЯ КОНКРЕТНЫХ РАССКАЗОВ ===')

# Получаем несколько рассказов для тестирования
stories = Story.objects.all()[:5]

if stories:
    for story in stories:
        try:
            change_url = reverse('admin:stories_story_change', args=[story.pk])
            print('✅ Рассказ \"{}\" (ID: {}) -> {}'.format(story.title, story.pk, change_url))
        except Exception as e:
            print('❌ Ошибка для рассказа \"{}\" (ID: {}): {}'.format(story.title, story.pk, e))
else:
    print('⚠️ Нет рассказов в базе данных')

print()
print('=== ТЕСТИРОВАНИЕ КОНКРЕТНОГО URL ===')

# Проверяем URL для рассказа 'Как святой Лука дочь спас'
luka_story = Story.objects.filter(title__icontains='Лука').first()
if luka_story:
    try:
        luka_url = reverse('admin:stories_story_change', args=[luka_story.pk])
        print('🎯 URL для рассказа о святом Луке: {}'.format(luka_url))
        print('📝 ID рассказа: {}'.format(luka_story.pk))
        print('📝 Slug рассказа: {}'.format(luka_story.slug))
    except Exception as e:
        print('❌ Ошибка для рассказа о Луке: {}'.format(e))
else:
    print('⚠️ Рассказ о святом Луке не найден')
"

echo.
echo ===============================================
echo 📋 ШАГ 2: Проверка настроек админки
echo ===============================================

python manage.py shell -c "
from django.contrib.admin.sites import site
from stories.models import Story
from stories.admin import StoryAdmin

print('=== ПРОВЕРКА НАСТРОЕК АДМИНКИ ===')

if Story in site._registry:
    admin_class = site._registry[Story]
    print('✅ Story зарегистрирована в админке')
    
    # Проверяем list_display
    list_display = getattr(admin_class, 'list_display', [])
    print('📊 list_display: {}'.format(list_display))
    
    # Проверяем list_display_links
    list_display_links = getattr(admin_class, 'list_display_links', None)
    print('🔗 list_display_links: {}'.format(list_display_links))
    
    # Проверяем методы админки
    has_change_view = hasattr(admin_class, 'change_view')
    has_changelist_view = hasattr(admin_class, 'changelist_view')
    
    print('🔧 change_view метод: {}'.format(has_change_view))
    print('🔧 changelist_view метод: {}'.format(has_changelist_view))
    
else:
    print('❌ Story НЕ зарегистрирована в админке!')
"

echo.
echo ===============================================
echo 📋 ШАГ 3: Временное исправление админки
echo ===============================================

echo Создаем исправленную версию админки...

REM Создаем backup старой админки
copy "stories\admin.py" "stories\admin_backup.py" >nul
echo ✅ Создан backup: stories\admin_backup.py

REM Добавляем исправления в админку
echo. >> stories\admin.py
echo # ============================================= >> stories\admin.py
echo # 🔧 ИСПРАВЛЕНИЕ ССЫЛОК В СПИСКЕ РАССКАЗОВ >> stories\admin.py
echo # ============================================= >> stories\admin.py
echo. >> stories\admin.py
echo # Переопределяем StoryAdmin для исправления ссылок >> stories\admin.py
echo from django.contrib import admin >> stories\admin.py
echo from django.utils.html import format_html >> stories\admin.py
echo. >> stories\admin.py
echo # Убираем старую регистрацию и создаем новую >> stories\admin.py
echo admin.site.unregister(Story) >> stories\admin.py
echo. >> stories\admin.py
echo @admin.register(Story) >> stories\admin.py
echo class StoryAdminFixed(admin.ModelAdmin): >> stories\admin.py
echo     list_display = [ >> stories\admin.py
echo         'title_link',  # Кастомная ссылка >> stories\admin.py
echo         'category', >> stories\admin.py
echo         'views_count', >> stories\admin.py
echo         'is_featured', >> stories\admin.py
echo         'is_published', >> stories\admin.py
echo         'created_at' >> stories\admin.py
echo     ] >> stories\admin.py
echo     list_display_links = None  # Отключаем автоматические ссылки >> stories\admin.py
echo     list_filter = ['is_published', 'is_featured', 'category', 'created_at'] >> stories\admin.py
echo     search_fields = ['title', 'description'] >> stories\admin.py
echo     prepopulated_fields = {'slug': ('title',)} >> stories\admin.py
echo     filter_horizontal = ['tags'] >> stories\admin.py
echo     list_per_page = 25 >> stories\admin.py
echo. >> stories\admin.py
echo     def title_link(self, obj): >> stories\admin.py
echo         \"\"\"Создает кликабельную ссылку на редактирование\"\"\" >> stories\admin.py
echo         from django.urls import reverse >> stories\admin.py
echo         from django.utils.html import format_html >> stories\admin.py
echo         url = reverse('admin:stories_story_change', args=[obj.pk]) >> stories\admin.py
echo         return format_html('<a href=\"{}\">{}</a>', url, obj.title) >> stories\admin.py
echo     title_link.short_description = 'Название' >> stories\admin.py
echo     title_link.admin_order_field = 'title' >> stories\admin.py

echo ✅ Исправления добавлены в stories\admin.py

echo.
echo ===============================================
echo 📋 ШАГ 4: Перезапуск сервера
echo ===============================================

echo Очищаем кеш...
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('✅ Кеш очищен')"

echo.
echo 🎯 ТЕСТИРОВАНИЕ:
echo 1. Откройте список рассказов: http://127.0.0.1:8000/admin/stories/story/
echo 2. Кликните на НАЗВАНИЕ любого рассказа
echo 3. Должна открыться форма редактирования
echo.
echo ⚠️ Если не работает - попробуйте:
echo    - Очистить кеш браузера (Ctrl+Shift+Del)
echo    - Перезагрузить страницу (F5)
echo    - Открыть в режиме инкогнито
echo.

echo Запускаем сервер с исправлениями...
python manage.py runserver
