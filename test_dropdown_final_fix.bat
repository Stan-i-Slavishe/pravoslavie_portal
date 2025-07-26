@echo off
echo.
echo =======================================================
echo   Тестируем исправление dropdown меню для мобильной версии
echo =======================================================
echo.

echo 1. Перезапускаем Django сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 >nul

echo 2. Собираем статические файлы...
python manage.py collectstatic --noinput

echo 3. Запускаем сервер...
echo.
echo ✅ ИСПРАВЛЕНИЯ:
echo    - Добавлен новый CSS файл mobile-dropdown-fix.css
echo    - Исправлены дублирующиеся ID: sectionsDropdown и userDropdown  
echo    - Настроены z-index значения для правильного наложения
echo    - Меню "admin" теперь имеет z-index: 1060
echo    - Меню "Разделы" имеет z-index: 1040
echo.
echo 🔧 Тестируйте в мобильной версии:
echo    1. Откройте DevTools (F12)
echo    2. Переключите в мобильный режим
echo    3. Попробуйте открыть меню "Разделы", затем "admin"
echo    4. Убедитесь, что нет наложения
echo.

python manage.py runserver 127.0.0.1:8000
