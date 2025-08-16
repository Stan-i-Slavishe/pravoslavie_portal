@echo off
echo ===== ДИАГНОСТИКА ПРОБЛЕМЫ С ВИДЕО =====
echo.

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo Запуск диагностики...
python diagnose_video_issue.py

pause
