@echo off
echo 🚀 АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ ПРОБЛЕМЫ СО СПИСКОМ РАССКАЗОВ
echo.

echo ===============================================
echo 📋 ШАГ 1: Проверка и исправление URL админки
echo ===============================================

REM Создаем скрипт для проверки URL
python manage.py shell -c "
import os
from django.urls import reverse
from django.contrib.admin.sites import site
from stories.models import Story

print('🔍 ДИАГНОСТИКА ПРОБЛЕМЫ URL...')

# Получаем правильные URL
try:
    list_url = reverse('admin:stories_story_changelist')
    add_url = reverse('admin:stories_story_add')
    admin_url = reverse('admin:index')
    
    print('✅ Правильные URL найдены:')
    print('   📚 Список рассказов:', list_url)
    print('   ➕ Добавить рассказ:', add_url)
    print('   🏠 Главная админки:', admin_url)
    
    # Проверяем количество рассказов
    total = Story.objects.count()
    print('📊 Всего рассказов в БД:', total)
    
    if total > 0:
        print('📝 Рассказы в БД:')
        for story in Story.objects.all()[:5]:
            story_url = reverse('admin:stories_story_change', args=[story.pk])
            print('   - {} (ID: {}) - {}'.format(story.title, story.pk, story_url))
    
    print()
    print('🎯 РЕШЕНИЕ ПРОБЛЕМЫ:')
    print('Вместо /admin/stories/story/')
    print('Используйте: {}'.format(list_url))
    
except Exception as e:
    print('❌ Ошибка:', e)
"

echo.
echo ===============================================
echo 📋 ШАГ 2: Исправление навигации админки
echo ===============================================

REM Очищаем кеш
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('✅ Кеш очищен')"

echo.
echo ===============================================
echo 📋 ШАГ 3: Создание правильных ссылок
echo ===============================================

echo 🔗 Правильные ссылки для закладок:
echo.
echo 📚 СПИСОК ВСЕХ РАССКАЗОВ:
echo    http://127.0.0.1:8000/admin/stories/story/
echo    (должен показывать таблицу со всеми рассказами)
echo.
echo ➕ ДОБАВИТЬ НОВЫЙ РАССКАЗ:
echo    http://127.0.0.1:8000/admin/stories/story/add/
echo.
echo 🏠 ГЛАВНАЯ АДМИНКИ:
echo    http://127.0.0.1:8000/admin/
echo    (найдите секцию ВИДЕО-РАССКАЗЫ и кликните Рассказы)
echo.

echo ===============================================
echo 🎯 ПОШАГОВАЯ ИНСТРУКЦИЯ
echo ===============================================
echo.
echo 1. Откройте: http://127.0.0.1:8000/admin/
echo 2. Войдите в админку (если не вошли)
echo 3. Найдите секцию "ВИДЕО-РАССКАЗЫ"
echo 4. Кликните на "Рассказы" в этой секции
echo 5. Должна открыться таблица со всеми рассказами
echo.
echo ⚠️ ВАЖНО: НЕ используйте боковую панель!
echo    Используйте главную страницу админки!
echo.

echo ===============================================
echo 🚀 ЗАПУСК СЕРВЕРА
echo ===============================================

echo Запускаем сервер...
echo После запуска откройте: http://127.0.0.1:8000/admin/
echo.

python manage.py runserver
