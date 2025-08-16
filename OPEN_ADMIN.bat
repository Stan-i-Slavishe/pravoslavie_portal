@echo off
echo ===== ОТКРЫВАЕМ DJANGO ADMIN =====
echo.

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo Создаем суперпользователя (если нужно)...
python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>nul

echo Запускаем сервер...
echo.
echo 🌐 Откройте в браузере: http://127.0.0.1:8000/admin/
echo 📝 Логин: admin
echo 🔑 Пароль: admin (или тот что вы установили)
echo.
echo 📍 Перейдите в: Stories -> Рассказы
echo 🔧 Найдите "Как святой Лука дочь спас"
echo ✏️ Добавьте YouTube URL, например:
echo    https://www.youtube.com/watch?v=dQw4w9WgXcQ
echo.

python manage.py runserver

pause
