@echo off
echo ===================================
echo МГНОВЕННОЕ ИСПРАВЛЕНИЕ YOUTUBE ID
echo ===================================

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate.bat

echo Исправляю YouTube ID прямо сейчас...
python fix_youtube_direct.py

echo.
echo Готово! Перезагрузите страницу в браузере.
echo Видео должно работать!

pause
