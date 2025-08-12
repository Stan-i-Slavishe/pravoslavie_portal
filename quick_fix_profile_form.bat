@echo off
echo ========================================
echo БЫСТРОЕ ИСПРАВЛЕНИЕ ФОРМЫ ПРОФИЛЯ
echo ========================================

echo.
echo Проблема: Поля формы не реагируют на клики
echo Решение: Применяем CSS и JavaScript исправления
echo.

echo 1. Создаем резервную копию...
if exist "accounts\templates\accounts\profile_edit_backup.html" (
    echo    ✓ Резервная копия уже существует
) else (
    copy "accounts\templates\accounts\profile_edit.html" "accounts\templates\accounts\profile_edit_backup.html"
    echo    ✓ Резервная копия создана
)

echo.
echo 2. Читаем оригинальный файл...
set "original_file=accounts\templates\accounts\profile_edit.html"
set "temp_file=temp_profile_edit.html"

echo.
echo 3. Применяем исправления...

REM Используем PowerShell для обработки файла
powershell -Command "$content = Get-Content '%original_file%' -Raw -Encoding UTF8; $content = $content -replace '</style>', (Get-Content 'profile_form_fix.css' -Raw) + '</style>'; $content = $content -replace '</script>', (Get-Content 'profile_form_fix.js' -Raw) + '</script>'; $content | Out-File '%temp_file%' -Encoding UTF8"

if exist "%temp_file%" (
    move "%temp_file%" "%original_file%"
    echo    ✓ CSS исправления добавлены
    echo    ✓ JavaScript исправления добавлены
) else (
    echo    ❌ Ошибка при применении исправлений
    echo.
    echo    РУЧНОЕ РЕШЕНИЕ:
    echo    1. Откройте accounts\templates\accounts\profile_edit.html
    echo    2. Добавьте содержимое profile_form_fix.css в блок style
    echo    3. Добавьте содержимое profile_form_fix.js в блок script
    goto end
)

echo.
echo 4. Перезапускаем сервер...
taskkill /F /IM python.exe 2>nul
timeout /t 1 /nobreak >nul

echo.
echo ========================================
echo ✅ ИСПРАВЛЕНИЕ ПРИМЕНЕНО!
echo ========================================
echo.
echo Что было исправлено:
echo • Убраны CSS блокировки pointer-events
echo • Добавлены JavaScript обработчики кликов  
echo • Исправлена z-index проблема
echo • Убраны конфликтующие анимации
echo.
echo Теперь запустите сервер:
echo python manage.py runserver
echo.
echo И обновите страницу в браузере (Ctrl+F5)
echo.

:end
pause
