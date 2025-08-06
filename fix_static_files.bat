@echo off
echo ========================================
echo   БЫСТРОЕ ИСПРАВЛЕНИЕ СТАТИКИ
echo ========================================

echo 1. Принудительная очистка статических файлов...
rmdir /s /q staticfiles 2>nul

echo 2. Создаем директории...
mkdir staticfiles 2>nul
mkdir staticfiles\css 2>nul
mkdir staticfiles\js 2>nul

echo 3. Собираем статические файлы с принудительной перезаписью...
python manage.py collectstatic --noinput --clear

echo 4. Проверяем результат...
if exist "staticfiles\css\mobile-burger-left-fix.css" (
    echo ✅ CSS файл скопирован в staticfiles
) else (
    echo ❌ CSS файл НЕ скопирован
)

if exist "staticfiles\js\mobile-burger-left-fix.js" (
    echo ✅ JS файл скопирован в staticfiles
) else (
    echo ❌ JS файл НЕ скопирован
)

echo 5. Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
start cmd /k "python manage.py runserver 127.0.0.1:8000"

echo ========================================
echo   СТАТИЧЕСКИЕ ФАЙЛЫ ОБНОВЛЕНЫ!
echo ========================================
echo Теперь протестируйте:
echo http://127.0.0.1:8000/shop/?type=subscription
echo F12 → Toggle Device → iPhone XR
echo Ctrl+Shift+R (принудительное обновление)

pause
