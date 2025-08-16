@echo off
echo 🚀 ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С ПЕРЕХОДАМИ В АДМИНКЕ
echo.

echo ===============================================
echo 📋 ШАГ 1: Временно отключаем строгие настройки безопасности
echo ===============================================

REM Создаем временный файл с исправленными настройками
echo # Временные настройки для исправления проблемы с переходами > temp_security_fix.py
echo # Добавьте эти строки в config/settings.py >> temp_security_fix.py
echo. >> temp_security_fix.py
echo # Временно отключаем строгие настройки для отладки >> temp_security_fix.py
echo SECURE_CROSS_ORIGIN_OPENER_POLICY = None >> temp_security_fix.py
echo SECURE_REFERRER_POLICY = None >> temp_security_fix.py
echo. >> temp_security_fix.py
echo # Разрешаем переходы в админке >> temp_security_fix.py
echo CSRF_COOKIE_SAMESITE = 'Lax' >> temp_security_fix.py
echo SESSION_COOKIE_SAMESITE = 'Lax' >> temp_security_fix.py
echo. >> temp_security_fix.py
echo # Отключаем проблемные заголовки >> temp_security_fix.py
echo SECURE_BROWSER_XSS_FILTER = False >> temp_security_fix.py

echo.
echo ===============================================
echo 📋 ШАГ 2: Проверяем URL-маршруты админки
echo ===============================================

python manage.py shell -c "
from django.urls import reverse
from django.contrib.admin.sites import site
from stories.models import Story

print('=== ПРОВЕРКА URL АДМИНКИ ===')
try:
    # Проверяем основные URL
    admin_url = reverse('admin:index')
    stories_list_url = reverse('admin:stories_story_changelist')
    print('✅ URL админки:', admin_url)
    print('✅ URL списка рассказов:', stories_list_url)
    
    # Проверяем URL конкретного рассказа
    story = Story.objects.first()
    if story:
        story_change_url = reverse('admin:stories_story_change', args=[story.pk])
        print('✅ URL редактирования рассказа:', story_change_url)
    else:
        print('⚠️ Нет рассказов в базе данных')
        
    print('✅ Все URL корректны')
except Exception as e:
    print('❌ Ошибка URL:', e)
"

echo.
echo ===============================================
echo 📋 ШАГ 3: Очищаем кеш и перезапускаем
echo ===============================================

python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('✅ Кеш очищен')"

echo.
echo 📋 СЛЕДУЮЩИЕ ШАГИ:
echo.
echo 1. Скопируйте содержимое файла temp_security_fix.py
echo 2. Добавьте эти настройки в конец файла config/settings.py
echo 3. Перезапустите сервер: python manage.py runserver
echo 4. Попробуйте снова перейти к редактированию рассказа
echo.
echo 📄 Настройки для добавления:
type temp_security_fix.py
echo.
pause
