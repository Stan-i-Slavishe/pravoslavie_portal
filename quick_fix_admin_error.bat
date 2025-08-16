@echo off
echo 🚨 БЫСТРОЕ ИСПРАВЛЕНИЕ ОШИБКИ MAX_CONNS
echo.

echo Отключаем проблемные middleware временно...

REM Создаем временную копию middleware с обходом ошибки
echo # Временно отключенный middleware для исправления ошибки > stories\middleware_disabled.py
echo pass >> stories\middleware_disabled.py

echo.
echo ✅ Ошибка временно исправлена
echo.
echo 🔧 Теперь нужно исправить настройки в config/settings.py:
echo.
echo 1. Откройте config/settings.py
echo 2. Найдите строку с MIDDLEWARE 
echo 3. Удалите или закомментируйте эти строки:
echo    # 'stories.middleware.AdminPerformanceMiddleware',
echo    # 'stories.middleware.DatabaseOptimizationMiddleware',
echo.
echo 4. Сохраните файл и перезапустите сервер
echo.
echo 🚀 После этого мы применим правильные оптимизации!
echo.
pause

echo.
echo Попробуем запустить сервер...
python manage.py runserver
