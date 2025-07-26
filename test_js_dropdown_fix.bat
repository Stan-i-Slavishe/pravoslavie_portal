@echo off
echo.
echo =======================================================
echo   JavaScript решение для dropdown меню
echo =======================================================
echo.

echo 1. Перезапускаем Django сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 >nul

echo 2. Собираем статические файлы...
python manage.py collectstatic --noinput

echo 3. Запускаем сервер...
echo.
echo ✅ ДОБАВЛЕНО:
echo    - JavaScript файл dropdown-smart-manager.js
echo    - Умное управление dropdown меню
echo    - Автоматическое определение конфликтов
echo    - Стратегии для разных размеров экранов
echo.
echo 🔧 Функции JavaScript решения:
echo    📱 < 576px: Закрытие других меню
echo    📱 < 768px: Смещение вниз  
echo    📱 < 992px: Умное смещение
echo    🖥️ >= 992px: Стандартное поведение
echo.
echo 🎯 ТЕСТИРУЙТЕ В МОБИЛЬНОЙ ВЕРСИИ:
echo    1. Откройте DevTools (F12)
echo    2. Переключите в мобильный режим (iPhone SE)
echo    3. Откройте меню "Разделы"
echo    4. Попробуйте открыть меню "admin"
echo    5. Меню будет автоматически управляться JavaScript
echo.
echo 🔍 Отладка в консоли:
echo    window.smartDropdownManager.debug()
echo    window.smartDropdownManager.getStatus()
echo.

python manage.py runserver 127.0.0.1:8000
