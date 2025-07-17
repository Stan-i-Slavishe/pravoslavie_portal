@echo off
echo Очищаем кеш браузера и исправляем HTTPS проблему...

REM Останавливаем все процессы Django
taskkill /F /IM python.exe 2>nul

REM Очищаем Django кеш
cd /d "E:\pravoslavie_portal"
call .venv\Scripts\activate.bat
python manage.py clearcache 2>nul

echo.
echo ИНСТРУКЦИИ ПО ОЧИСТКЕ БРАУЗЕРА:
echo.
echo Chrome: Ctrl+Shift+Delete - выберите "Все время", отметьте все галочки
echo Firefox: Ctrl+Shift+Delete - выберите "Все", отметьте все галочки  
echo Edge: Ctrl+Shift+Delete - выберите "Все время", отметьте все галочки
echo.
echo После очистки используйте ТОЛЬКО HTTP адреса:
echo http://127.0.0.1:8000 или http://localhost:8000
echo.
echo НЕ ИСПОЛЬЗУЙТЕ https://
echo.
pause
