@echo off
echo "Перезапуск Django сервера для применения изменений календаря..."
cd /d "E:\pravoslavie_portal"

echo "Остановка текущего сервера (если запущен)..."
taskkill /F /IM python.exe /T 2>nul

echo "Очистка кеша..."
if exist "__pycache__" rmdir /s /q "__pycache__"
for /d %%i in (*) do (
    if exist "%%i\__pycache__" rmdir /s /q "%%i\__pycache__"
)

echo "Применение миграций (если есть)..."
python manage.py makemigrations pwa
python manage.py migrate

echo "Запуск сервера..."
echo "Календарь будет доступен по адресу: http://127.0.0.1:8000/pwa/daily-calendar/"
echo "Проверьте 29 августа - он должен быть фиолетовым (постный день)"
echo.
python manage.py runserver
