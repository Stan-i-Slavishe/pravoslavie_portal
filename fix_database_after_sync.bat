@echo off
echo 🔧 ИСПРАВЛЕНИЕ БАЗЫ ДАННЫХ ПОСЛЕ СИНХРОНИЗАЦИИ
echo ===============================================

echo 📊 Проверяем статус миграций...
python manage.py showmigrations

echo.
echo 🔄 Создаем новые миграции (если нужно)...
python manage.py makemigrations

echo.
echo 📥 Применяем все миграции...
python manage.py migrate

echo.
echo 🧹 Собираем статические файлы...
python manage.py collectstatic --noinput

echo.
echo ✅ ГОТОВО! База данных обновлена.
echo.
echo 🚀 Теперь можно запустить сервер:
echo python manage.py runserver

pause
