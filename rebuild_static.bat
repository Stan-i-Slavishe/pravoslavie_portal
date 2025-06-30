@echo off
echo 🧹 Очистка и пересборка статических файлов...

echo.
echo ⭕ Удаляем старые файлы...
rmdir /s /q staticfiles 2>nul

echo.
echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

echo.
echo ✅ Готово! Статические файлы обновлены.
echo.
echo 🚀 Теперь можно запускать: python manage.py runserver
pause