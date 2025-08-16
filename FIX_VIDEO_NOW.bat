@echo off
echo ===== БЫСТРОЕ ИСПРАВЛЕНИЕ ВИДЕО =====
echo.

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo Исправляем видео...
python fix_video_now.py

echo.
echo Готово! Теперь обновите страницу в браузере!
pause
