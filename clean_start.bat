@echo off
echo 🔧 ПОЛНОЕ ОТКЛЮЧЕНИЕ системы безопасности
echo.

cd /d "E:\pravoslavie_portal"

echo 🔄 Восстановление базового settings.py...

REM Создаем чистый settings.py без middleware безопасности
echo # Временные настройки без middleware безопасности > config\settings_clean.py
echo from config.settings_backup import * >> config\settings_clean.py
echo. >> config\settings_clean.py
echo # Принудительно переопределяем MIDDLEWARE без безопасности >> config\settings_clean.py
echo MIDDLEWARE = [ >> config\settings_clean.py
echo     'django.middleware.security.SecurityMiddleware', >> config\settings_clean.py
echo     'whitenoise.middleware.WhiteNoiseMiddleware', >> config\settings_clean.py
echo     'django.contrib.sessions.middleware.SessionMiddleware', >> config\settings_clean.py
echo     'django.middleware.common.CommonMiddleware', >> config\settings_clean.py
echo     'django.middleware.csrf.CsrfViewMiddleware', >> config\settings_clean.py
echo     'django.contrib.auth.middleware.AuthenticationMiddleware', >> config\settings_clean.py
echo     'django.contrib.messages.middleware.MessageMiddleware', >> config\settings_clean.py
echo     'django.middleware.clickjacking.XFrameOptionsMiddleware', >> config\settings_clean.py
echo     'allauth.account.middleware.AccountMiddleware', >> config\settings_clean.py
echo ] >> config\settings_clean.py
echo. >> config\settings_clean.py
echo # Локальное кеширование >> config\settings_clean.py
echo CACHES = { >> config\settings_clean.py
echo     'default': { >> config\settings_clean.py
echo         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', >> config\settings_clean.py
echo         'LOCATION': 'unique-snowflake', >> config\settings_clean.py
echo     } >> config\settings_clean.py
echo } >> config\settings_clean.py

copy config\settings_clean.py config\settings.py

echo ✅ Настройки очищены от middleware безопасности
echo 🚀 Запуск чистого сервера...
python manage.py runserver

pause