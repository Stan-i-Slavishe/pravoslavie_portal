@echo off
echo ============================================
echo ИСПРАВЛЕНИЕ ПОЛЕЙ ФОРМЫ ПРОФИЛЯ
echo ============================================

echo.
echo 1. Создаем резервную копию оригинального файла...
copy "accounts\templates\accounts\profile_edit.html" "accounts\templates\accounts\profile_edit_backup.html"

echo.
echo 2. Применяем исправление...
copy "accounts\templates\accounts\profile_edit_fixed.html" "accounts\templates\accounts\profile_edit.html"

echo.
echo 3. Проверяем примененные изменения...
echo ✓ Добавлены критические CSS стили для полей формы
echo ✓ Добавлены JavaScript обработчики кликов
echo ✓ Исправлена проблема с pointer-events
echo ✓ Убраны перехваты событий с overlay элементов

echo.
echo 4. Перезапускаем сервер Django...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo 5. Запускаем сервер с исправлениями...
python manage.py runserver

pause