@echo off
echo Останавливаем все процессы Python...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo Ждем 2 секунды...
timeout /t 2 /nobreak >nul

echo Удаляем временные файлы SQLite...
if exist "db.sqlite3-wal" del "db.sqlite3-wal"
if exist "db.sqlite3-shm" del "db.sqlite3-shm"

echo Перезапускаем Django сервер...
python manage.py runserver

pause
