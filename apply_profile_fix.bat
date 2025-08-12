@echo off
echo ========================================
echo АЛЬТЕРНАТИВНОЕ ИСПРАВЛЕНИЕ ФОРМЫ
echo ========================================

echo Применяем готовый исправленный файл...

if exist "accounts\templates\accounts\profile_edit_fixed.html" (
    copy "accounts\templates\accounts\profile_edit_fixed.html" "accounts\templates\accounts\profile_edit.html"
    echo ✓ Исправленный файл применен
) else (
    echo ❌ Файл profile_edit_fixed.html не найден
    echo.
    echo РУЧНОЕ РЕШЕНИЕ:
    echo 1. Откройте accounts\templates\accounts\profile_edit.html
    echo 2. Найдите все .form-control и добавьте:
    echo    pointer-events: auto !important;
    echo    z-index: 10 !important;
    goto end
)

echo.
echo Запустите сервер:
echo python manage.py runserver
echo.
echo И обновите страницу: Ctrl+F5

:end
pause
