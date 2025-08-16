@echo off
echo 🚨 КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С URL АДМИНКИ
echo.

echo ===============================================
echo 📋 ШАГ 1: Остановка сервера и диагностика
echo ===============================================

echo В терминале с сервером нажмите Ctrl+C чтобы остановить его
echo Затем запустите эту диагностику:
pause

python manage.py shell -c "
print('=== КРИТИЧЕСКАЯ ДИАГНОСТИКА URL АДМИНКИ ===')

from django.urls import reverse, NoReverseMatch
from django.contrib.admin.sites import site
from stories.models import Story

# Проверяем базовую регистрацию
print('1. Проверка регистрации модели Story...')
if Story in site._registry:
    print('✅ Story зарегистрирована в админке')
    admin_class = site._registry[Story]
    print('   Класс админки:', admin_class.__class__.__name__)
else:
    print('❌ КРИТИЧЕСКАЯ ОШИБКА: Story НЕ зарегистрирована!')

# Проверяем URL паттерны
print()
print('2. Проверка URL паттернов...')
try:
    changelist_url = reverse('admin:stories_story_changelist')
    print('✅ URL списка найден:', changelist_url)
except NoReverseMatch as e:
    print('❌ ОШИБКА URL списка:', e)

try:
    add_url = reverse('admin:stories_story_add')
    print('✅ URL добавления найден:', add_url)
except NoReverseMatch as e:
    print('❌ ОШИБКА URL добавления:', e)

# Проверяем URL для конкретного объекта
print()
print('3. Проверка URL редактирования...')
stories = Story.objects.all()[:3]
for story in stories:
    try:
        change_url = reverse('admin:stories_story_change', args=[story.pk])
        print('✅ {}: {}'.format(story.title, change_url))
    except Exception as e:
        print('❌ Ошибка для {}: {}'.format(story.title, e))

# Проверяем настройки админки
print()
print('4. Проверка настроек админки...')
if Story in site._registry:
    admin_class = site._registry[Story]
    
    # Список отображаемых полей
    list_display = getattr(admin_class, 'list_display', None)
    print('   list_display:', list_display)
    
    # Поля-ссылки
    list_display_links = getattr(admin_class, 'list_display_links', None)
    print('   list_display_links:', list_display_links)
    
    # Проверяем методы
    methods = [method for method in dir(admin_class) if not method.startswith('_')]
    print('   Методы админки:', len(methods))

print()
print('=== АНАЛИЗ ЗАВЕРШЕН ===')
"

echo.
echo ===============================================
echo 📋 ШАГ 2: Полная переустановка админки Stories
echo ===============================================

echo Создаем backup текущей админки...
copy "stories\admin.py" "stories\admin_broken.py" >nul
echo ✅ Backup создан: stories\admin_broken.py

echo.
echo Создаем полностью новую админку...

REM Создаем минимальную рабочую админку
echo # ============================================= > stories\admin_minimal.py
echo # МИНИМАЛЬНАЯ РАБОЧАЯ АДМИНКА ДЛЯ ДИАГНОСТИКИ >> stories\admin_minimal.py
echo # ============================================= >> stories\admin_minimal.py
echo. >> stories\admin_minimal.py
echo from django.contrib import admin >> stories\admin_minimal.py
echo from .models import Story >> stories\admin_minimal.py
echo. >> stories\admin_minimal.py
echo # Отменяем старую регистрацию >> stories\admin_minimal.py
echo try: >> stories\admin_minimal.py
echo     admin.site.unregister(Story) >> stories\admin_minimal.py
echo except admin.sites.NotRegistered: >> stories\admin_minimal.py
echo     pass >> stories\admin_minimal.py
echo. >> stories\admin_minimal.py
echo # Простейшая регистрация >> stories\admin_minimal.py
echo @admin.register(Story) >> stories\admin_minimal.py
echo class StoryAdminMinimal(admin.ModelAdmin): >> stories\admin_minimal.py
echo     list_display = ['title', 'category', 'is_published', 'created_at'] >> stories\admin_minimal.py
echo     list_display_links = ['title']  # Явно указываем ссылку >> stories\admin_minimal.py
echo     list_filter = ['is_published', 'category'] >> stories\admin_minimal.py
echo     search_fields = ['title'] >> stories\admin_minimal.py
echo     readonly_fields = ['created_at', 'updated_at'] >> stories\admin_minimal.py
echo. >> stories\admin_minimal.py
echo print('🔧 Минимальная админка Stories загружена') >> stories\admin_minimal.py

echo ✅ Создана минимальная админка: stories\admin_minimal.py

echo.
echo ===============================================
echo 📋 ШАГ 3: Замена админки
echo ===============================================

echo Заменяем админку на минимальную версию...
copy "stories\admin_minimal.py" "stories\admin.py" >nul
echo ✅ Админка заменена на минимальную версию

echo.
echo ===============================================
echo 📋 ШАГ 4: Очистка и перезапуск
echo ===============================================

echo Очищаем все кеши...
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('✅ Кеш очищен')"

echo.
echo Удаляем скомпилированные Python файлы...
del /s /q "stories\__pycache__\*.pyc" 2>nul
del /s /q "stories\*.pyc" 2>nul
echo ✅ Скомпилированные файлы удалены

echo.
echo ===============================================
echo 🚀 ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЯ
echo ===============================================

echo 🎯 ПОСЛЕ ЗАПУСКА СЕРВЕРА ПРОВЕРЬТЕ:
echo.
echo 1. Откройте: http://127.0.0.1:8000/admin/
echo 2. Найдите секцию ВИДЕО-РАССКАЗЫ → Рассказы
echo 3. Должен открыться СПИСОК всех рассказов
echo 4. Клик на название должен открыть редактирование
echo.
echo ⚠️ ВАЖНО: Теперь используйте ТОЛЬКО главную админки!
echo    НЕ используйте боковую панель!
echo.

echo Запускаем сервер с исправленной админкой...
python manage.py runserver
