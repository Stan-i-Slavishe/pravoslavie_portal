@echo off
echo ===================================
echo ПРИНУДИТЕЛЬНОЕ ОБНОВЛЕНИЕ ШАБЛОНОВ
echo ===================================
echo.

cd /d "%~dp0"

echo Очистка кеша Django...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

python manage.py collectstatic --noinput --clear
echo.

echo Перезапуск сервера...
echo Нажмите Ctrl+C чтобы остановить текущий сервер, затем запустите:
echo python manage.py runserver
echo.

echo ===================================
echo После перезапуска сервера:
echo 1. Обновите страницу с Ctrl+F5
echo 2. Проверьте кликабельность заголовка "Мои плейлисты"
echo 3. Ищите иконки управления в сайдбаре
echo ===================================
pause
