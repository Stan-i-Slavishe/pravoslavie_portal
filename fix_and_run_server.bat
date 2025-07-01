@echo off
echo ========================================
echo     ИСПРАВЛЕНИЕ И ЗАПУСК СЕРВЕРА
echo ========================================
echo.

echo 🗂️ Переходим в директорию проекта...
cd /d "E:\pravoslavie_portal"

echo 🔧 Активируем виртуальное окружение...
call .venv\Scripts\activate

echo ✅ Файл manage.py исправлен!
echo    Убран лишний символ "п" из первой строки

echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

echo 🚀 Запускаем Django сервер...
echo.
echo 🌐 Сервер будет доступен по адресу: http://127.0.0.1:8000
echo 💬 Теперь на карточках рассказов должны отображаться комментарии!
echo.
python manage.py runserver

pause
