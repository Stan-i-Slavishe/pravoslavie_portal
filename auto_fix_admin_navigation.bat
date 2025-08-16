@echo off
echo 🔧 АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ НАСТРОЕК БЕЗОПАСНОСТИ
echo.

echo Добавляем исправления в config/settings.py...

REM Создаем резервную копию
copy "config\settings.py" "config\settings_backup.py" >nul
echo ✅ Создана резервная копия: config/settings_backup.py

REM Добавляем исправления в конец файла
echo. >> config\settings.py
echo # ============================================= >> config\settings.py
echo # 🚀 ИСПРАВЛЕНИЕ ПРОБЛЕМ С ПЕРЕХОДАМИ В АДМИНКЕ >> config\settings.py
echo # ============================================= >> config\settings.py
echo. >> config\settings.py
echo # Временно отключаем строгие настройки для исправления переходов >> config\settings.py
echo SECURE_CROSS_ORIGIN_OPENER_POLICY = None >> config\settings.py
echo SECURE_REFERRER_POLICY = None >> config\settings.py
echo. >> config\settings.py
echo # Разрешаем переходы в админке >> config\settings.py
echo CSRF_COOKIE_SAMESITE = 'Lax' >> config\settings.py
echo SESSION_COOKIE_SAMESITE = 'Lax' >> config\settings.py
echo. >> config\settings.py
echo # Отключаем проблемные заголовки для админки >> config\settings.py
echo SECURE_BROWSER_XSS_FILTER = False >> config\settings.py
echo. >> config\settings.py
echo # Дополнительные настройки для админки >> config\settings.py
echo if DEBUG: >> config\settings.py
echo     # В режиме разработки отключаем все строгие настройки >> config\settings.py
echo     SECURE_SSL_REDIRECT = False >> config\settings.py
echo     SESSION_COOKIE_SECURE = False >> config\settings.py
echo     CSRF_COOKIE_SECURE = False >> config\settings.py
echo     SECURE_HSTS_SECONDS = 0 >> config\settings.py
echo. >> config\settings.py
echo print('🔧 Настройки безопасности для админки применены!') >> config\settings.py

echo ✅ Настройки добавлены в config/settings.py

echo.
echo ===============================================
echo 📋 ПЕРЕЗАПУСК СЕРВЕРА С ИСПРАВЛЕНИЯМИ
echo ===============================================

echo Очищаем кеш...
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('✅ Кеш очищен')"

echo.
echo 🚀 Запускаем сервер с исправленными настройками...
echo.
echo 📋 ТЕСТИРОВАНИЕ:
echo 1. Откройте админку: http://127.0.0.1:8000/admin/
echo 2. Перейдите в Stories (Рассказы)
echo 3. Кликните на любой рассказ для редактирования
echo 4. Страница должна открыться без перезагрузки
echo.
echo ⚠️ Если проблема сохраняется - нажмите Ctrl+C и сообщите
echo.

python manage.py runserver
