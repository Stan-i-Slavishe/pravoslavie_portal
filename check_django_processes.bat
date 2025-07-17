@echo off
echo 🔍 Поиск процессов Django
echo.

echo Ищем процессы Python:
tasklist | findstr python

echo.
echo Ищем процессы с "manage":
tasklist | findstr manage

echo.
echo Ищем процессы Django:
tasklist | findstr django

echo.
echo Ищем процессы runserver:
netstat -ano | findstr :8000

pause
