@echo off
REM Скрипт проверки применения исправлений мобильной навигации

echo 🔧 Проверка исправлений мобильной навигации...
echo ===============================================

REM Проверяем наличие нового CSS файла
if exist "static\css\mobile-icons-spacing-fix.css" (
    echo ✅ Файл mobile-icons-spacing-fix.css найден
    for %%A in ("static\css\mobile-icons-spacing-fix.css") do echo    Размер: %%~zA байт
) else (
    echo ❌ Файл mobile-icons-spacing-fix.css НЕ найден
)

REM Проверяем подключение в base.html
findstr /C:"mobile-icons-spacing-fix.css" "templates\base.html" >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ CSS файл подключен в base.html
) else (
    echo ❌ CSS файл НЕ подключен в base.html
)

REM Проверяем обновления в mobile-burger-menu.css  
findstr /C:"ИСПРАВЛЕНИЕ НАЛОЖЕНИЯ КОРЗИНЫ И БУРГЕРА" "static\css\mobile-burger-menu.css" >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Исправления добавлены в mobile-burger-menu.css
) else (
    echo ❌ Исправления НЕ найдены в mobile-burger-menu.css
)

echo.
echo 🚀 Для применения изменений:
echo 1. python manage.py collectstatic --noinput
echo 2. Перезапустите сервер
echo 3. Очистите кеш браузера (Ctrl+F5)
echo.
echo 📱 Тестируйте на экранах шире 992px - должен исчезнуть бургер
echo 📱 Тестируйте на мобильных - корзина слева, бургер справа

pause
