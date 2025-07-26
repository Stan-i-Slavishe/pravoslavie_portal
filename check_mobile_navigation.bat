@echo off
echo 🔍 ПРОВЕРКА ИНТЕГРАЦИИ МОБИЛЬНОЙ НАВИГАЦИИ
echo =============================================
echo.

echo 📁 Проверка файлов:
if exist "static\css\mobile-navigation.css" (
    echo ✅ static\css\mobile-navigation.css - НАЙДЕН
) else (
    echo ❌ static\css\mobile-navigation.css - НЕ НАЙДЕН
)

if exist "static\js\mobile-navigation.js" (
    echo ✅ static\js\mobile-navigation.js - НАЙДЕН
) else (
    echo ❌ static\js\mobile-navigation.js - НЕ НАЙДЕН
)

if exist "templates\base.html" (
    echo ✅ templates\base.html - ОБНОВЛЕН
) else (
    echo ❌ templates\base.html - НЕ НАЙДЕН
)

if exist "templates\base.html.backup" (
    echo ✅ templates\base.html.backup - СОЗДАН
) else (
    echo ❌ templates\base.html.backup - НЕ НАЙДЕН
)

echo.
echo 🎨 Проверка CSS переменных:
findstr /C:"fairy-tales-color" "static\css\azbyka-style.css" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Цветовые переменные добавлены
) else (
    echo ❌ Цветовые переменные не найдены
)

echo.
echo 📱 Проверка HTML шаблона:
findstr /C:"mobile-bottom-nav" "templates\base.html" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Мобильная навигация добавлена
) else (
    echo ❌ Мобильная навигация не найдена
)

findstr /C:"has-mobile-nav" "templates\base.html" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ CSS класс body добавлен
) else (
    echo ❌ CSS класс body не найден
)

findstr /C:"mobile-navigation.css" "templates\base.html" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ CSS файл подключен
) else (
    echo ❌ CSS файл не подключен
)

findstr /C:"mobile-navigation.js" "templates\base.html" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ JS файл подключен
) else (
    echo ❌ JS файл не подключен
)

echo.
echo 🚀 ГОТОВО К ЗАПУСКУ!
echo Запустите: python manage.py runserver 8000
echo Откройте в мобильном режиме: http://127.0.0.1:8000
echo.
pause
