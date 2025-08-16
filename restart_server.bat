@echo off
echo ===== CSP ИСПРАВЛЕН! ПЕРЕЗАПУСК СЕРВЕРА =====
echo.

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo ✅ CSP_FRAME_SRC добавлен для YouTube
echo 🔄 Перезапускаем Django сервер...
echo.

taskkill /f /im python.exe 2>nul
timeout /t 2

echo 🚀 Запускаем сервер...
echo.
echo 📺 Теперь откройте:
echo    http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/
echo.
echo ✅ YouTube видео должно работать!
echo.

python manage.py runserver
