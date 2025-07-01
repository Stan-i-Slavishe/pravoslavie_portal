@echo off
echo ========================================
echo   ПРИМЕНЕНИЕ ИЗМЕНЕНИЙ CSS/СТАТИКИ
echo ========================================
echo.

echo 🗂️ Переходим в директорию проекта...
cd /d "E:\pravoslavie_portal"

echo 🔧 Активируем виртуальное окружение...
call venv\Scripts\activate

echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

echo ✅ Статические файлы обновлены!
echo.
echo 🔄 Обновите страницу в браузере (Ctrl+F5 для принудительного обновления)
echo 🌐 http://127.0.0.1:8000/stories/malyshka/
echo.

pause
