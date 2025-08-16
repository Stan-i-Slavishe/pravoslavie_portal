@echo off
echo ===============================
echo УСТАНОВКА ТЕСТОВЫХ ВИДЕО
echo ===============================

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate.bat

echo Устанавливаю тестовые YouTube видео...
echo Эти видео точно работают и разрешают встраивание!
echo.

python set_test_videos.py

echo.
echo ✅ Готово! 
echo.
echo 🎬 Теперь проверьте любой рассказ:
echo    http://127.0.0.1:8000/stories/dva-syna/
echo    http://127.0.0.1:8000/stories/pochti-pokojnik/
echo.
echo Видео должно заработать!

pause
