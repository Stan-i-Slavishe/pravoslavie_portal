@echo off
echo ===============================
echo ПОЛНАЯ ДИАГНОСТИКА YOUTUBE ID
echo ===============================

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate.bat

echo Ищем все YouTube ID в базе данных...
python find_all_youtube.py

echo.
echo ======================================
echo ПРИНУДИТЕЛЬНЫЙ ПЕРЕЗАПУСК СЕРВЕРА
echo ======================================
echo.
echo Останавливаю старый сервер (если работает)...
taskkill /f /im python.exe 2>nul

echo.
echo Запускаю новый сервер с обновленными данными...
python manage.py runserver

pause
