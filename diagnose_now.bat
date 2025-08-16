@echo off
echo ==============================
echo ДИАГНОСТИКА И ИСПРАВЛЕНИЕ
echo ==============================

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate.bat

echo Диагностируем проблему...
python diagnose_video.py

echo.
echo Теперь перезагрузите страницу!
echo Если видео все еще не работает, проблема в шаблоне.

pause
