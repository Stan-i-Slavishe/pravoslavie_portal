@echo off
echo ===============================
echo ИСПОЛЬЗУЕМ РАБОЧЕЕ ВИДЕО
echo ===============================

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate.bat

echo Устанавливаем рабочий YouTube ID...
python use_working_video.py

echo.
echo ✅ Готово! Обновите страницу в браузере.
echo Видео должно заработать!

pause
