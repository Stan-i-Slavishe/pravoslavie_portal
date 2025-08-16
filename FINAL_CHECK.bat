@echo off
echo ===== ФИНАЛЬНАЯ ПРОВЕРКА =====
echo.

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

python final_check.py

echo.
echo ===== ЗАПУСК СЕРВЕРА ДЛЯ ПРОВЕРКИ =====
echo.
echo Сейчас откроется сервер Django.
echo Перейдите по адресу:
echo http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/
echo.
echo И проверьте:
echo 1. Показывается ли видео Rick Astley?
echo 2. Есть ли ошибки в консоли браузера (F12)?
echo 3. Что находится в div.video-container?
echo.

python manage.py runserver
