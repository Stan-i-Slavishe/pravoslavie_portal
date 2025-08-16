@echo off
echo 🚨 ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С URL СПИСКА РАССКАЗОВ
echo.

echo ===============================================
echo 📋 ШАГ 1: Диагностика текущих URL
echo ===============================================

python manage.py shell -c "
from django.urls import reverse
from django.contrib.admin.sites import site
from stories.models import Story

print('=== АНАЛИЗ URL ПРОБЛЕМЫ ===')

# Правильные URL для админки
try:
    correct_list_url = reverse('admin:stories_story_changelist')
    print('✅ ПРАВИЛЬНЫЙ URL списка рассказов:', correct_list_url)
except Exception as e:
    print('❌ Ошибка получения URL списка:', e)

try:
    add_url = reverse('admin:stories_story_add')
    print('✅ URL добавления рассказа:', add_url)
except Exception as e:
    print('❌ Ошибка URL добавления:', e)

# Проверяем, есть ли рассказ 'Стул' и его ID
stul_story = Story.objects.filter(title='Стул').first()
if stul_story:
    change_url = reverse('admin:stories_story_change', args=[stul_story.pk])
    print('📝 URL редактирования Стул (ID {}): {}'.format(stul_story.pk, change_url))
    print('⚠️ ПРОБЛЕМА: URL /admin/stories/story/ ведет к этому рассказу!')
else:
    print('📝 Рассказ Стул не найден в БД')

print()
print('=== РЕШЕНИЕ ===')
print('1. Правильный URL списка: /admin/stories/story/ -> должен быть changelist')
print('2. Текущий URL: /admin/stories/story/ -> ведет к change конкретного объекта')
print('3. Нужно исправить маршрутизацию или настройки админки')
"

echo.
echo ===============================================
echo 📋 ШАГ 2: Проверка настроек админки
echo ===============================================

python manage.py shell -c "
from django.contrib.admin.sites import site
from stories.models import Story
from stories.admin import StoryAdmin

print('=== ПРОВЕРКА РЕГИСТРАЦИИ АДМИНКИ ===')

if Story in site._registry:
    admin_class = site._registry[Story]
    print('✅ Story зарегистрирована в админке')
    print('📋 Класс админки:', admin_class.__class__.__name__)
    
    # Проверяем основные настройки
    print('📊 list_display:', getattr(admin_class, 'list_display', 'по умолчанию'))
    print('🔍 search_fields:', getattr(admin_class, 'search_fields', 'не установлено'))
    print('📄 list_per_page:', getattr(admin_class, 'list_per_page', 'по умолчанию'))
    
    # Проверяем методы
    print('🔧 get_urls метод:', hasattr(admin_class, 'get_urls'))
    print('🔧 changelist_view метод:', hasattr(admin_class, 'changelist_view'))
else:
    print('❌ Story НЕ зарегистрирована в админке!')
"

echo.
echo ===============================================
echo 📋 ШАГ 3: Очистка кеша и проверка URL
echo ===============================================

echo Очищаем кеш...
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('✅ Кеш очищен')"

echo.
echo ===============================================
echo 🔧 БЫСТРОЕ ИСПРАВЛЕНИЕ
echo ===============================================

echo Попробуйте эти URL в браузере:
echo.
echo 📚 Список всех рассказов:
echo    http://127.0.0.1:8000/admin/stories/story/
echo.
echo ➕ Добавить новый рассказ:
echo    http://127.0.0.1:8000/admin/stories/story/add/
echo.
echo 📝 Главная админки:
echo    http://127.0.0.1:8000/admin/
echo.
echo 🎯 РЕКОМЕНДАЦИИ:
echo 1. Перейдите сначала на главную админки: http://127.0.0.1:8000/admin/
echo 2. Найдите секцию ВИДЕО-РАССКАЗЫ
echo 3. Кликните на 'Рассказы' в этой секции
echo 4. Должен открыться список всех рассказов
echo.
pause

echo.
echo Перезапускаем сервер для применения изменений...
python manage.py runserver
