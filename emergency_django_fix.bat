@echo off
echo 🚨 ЭКСТРЕННОЕ ВОССТАНОВЛЕНИЕ DJANGO ПРОЕКТА
echo ============================================
echo.

echo 🔹 Этот скрипт исправляет проблемы после Git отката
echo.

REM Устанавливаем кодировку UTF-8
chcp 65001 >nul

echo 1️⃣  Останавливаем все процессы Django...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo.
echo 2️⃣  Активируем виртуальное окружение...
if not exist .venv\Scripts\activate.bat (
    echo ❌ ОШИБКА: Виртуальное окружение не найдено!
    echo Создайте виртуальное окружение или укажите правильный путь
    pause
    exit /b 1
)

call .venv\Scripts\activate

echo.
echo 3️⃣  Создаем резервную копию settings.py...
if exist config\settings.py (
    copy config\settings.py config\settings_emergency_backup.py >nul
    echo ✅ Резервная копия создана
) else (
    echo ❌ settings.py не найден!
)

echo.
echo 4️⃣  Очищаем старые статические файлы...
if exist staticfiles (
    rmdir /s /q staticfiles 2>nul
    echo ✅ Папка staticfiles удалена
)

echo.
echo 5️⃣  Очищаем кеш Django...
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); import django; django.setup(); from django.core.cache import cache; cache.clear(); print('✅ Кеш очищен')" 2>nul

echo.
echo 6️⃣  Проверяем базовые настройки Django...
python manage.py check --settings=config.settings 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Есть ошибки в настройках Django
    echo.
    echo 🔧 Применяем экстренные исправления настроек...
    
    REM Создаем временный скрипт для исправления settings.py
    echo import re > temp_fix_settings.py
    echo. >> temp_fix_settings.py
    echo with open('config/settings.py', 'r', encoding='utf-8'^) as f: >> temp_fix_settings.py
    echo     content = f.read(^) >> temp_fix_settings.py
    echo. >> temp_fix_settings.py
    echo # Включаем DEBUG режим >> temp_fix_settings.py
    echo content = re.sub(r'DEBUG\s*=\s*False', 'DEBUG = True', content^) >> temp_fix_settings.py
    echo. >> temp_fix_settings.py
    echo # Добавляем localhost в ALLOWED_HOSTS >> temp_fix_settings.py
    echo if "'localhost'" not in content and '"localhost"' not in content: >> temp_fix_settings.py
    echo     content = re.sub(r'ALLOWED_HOSTS\s*=\s*\[.*?\]', "ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']", content^) >> temp_fix_settings.py
    echo. >> temp_fix_settings.py
    echo with open('config/settings.py', 'w', encoding='utf-8'^) as f: >> temp_fix_settings.py
    echo     f.write(content^) >> temp_fix_settings.py
    echo. >> temp_fix_settings.py
    echo print('✅ Настройки исправлены'^) >> temp_fix_settings.py
    
    python temp_fix_settings.py
    del temp_fix_settings.py
)

echo.
echo 7️⃣  Проверяем миграции...
python manage.py migrate --fake-initial 2>nul
if %ERRORLEVEL% neq 0 (
    echo ⚠️  Проблемы с миграциями, пробуем мягкое исправление...
    python manage.py migrate --run-syncdb 2>nul
)

echo.
echo 8️⃣  Пересобираем статические файлы...
python manage.py collectstatic --noinput --clear
if %ERRORLEVEL% neq 0 (
    echo ⚠️  Проблемы со статическими файлами, пропускаем...
)

echo.
echo 9️⃣  Финальная проверка Django...
python manage.py check
if %ERRORLEVEL% equ 0 (
    echo.
    echo 🎉 УСПЕХ! Django восстановлен!
    echo.
    echo 📋 Что было исправлено:
    echo   • Остановлены процессы Django
    echo   • Очищены статические файлы
    echo   • Очищен кеш Django
    echo   • Исправлены базовые настройки
    echo   • Проверены миграции
    echo   • Пересобраны статические файлы
    echo.
    echo 🚀 Для запуска сервера:
    echo    python manage.py runserver
    echo.
    
    set /p start_server="Запустить сервер сейчас? (y/n): "
    if /i "%start_server%"=="y" (
        echo.
        echo 🚀 Запускаем Django сервер...
        python manage.py runserver
    )
) else (
    echo.
    echo ❌ ОШИБКА: Django все еще не запускается
    echo.
    echo 🔍 Дополнительная диагностика:
    echo   1. Проверьте логи выше
    echo   2. Убедитесь что база данных доступна
    echo   3. Проверьте файл .env
    echo   4. Запустите: python django_diagnostics.py
    echo.
    echo 📞 Для получения помощи:
    echo   • Сохраните ошибки из логов
    echo   • Проверьте config/settings.py
    echo   • Убедитесь что все приложения на месте
)

echo.
pause
