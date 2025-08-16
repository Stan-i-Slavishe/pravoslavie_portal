@echo off
chcp 65001 >nul
title Исправление админки - Православный портал
color 0A

echo.
echo ═══════════════════════════════════════
echo 🛠️  ИСПРАВЛЕНИЕ АДМИНКИ DJANGO
echo ═══════════════════════════════════════
echo.

cd /d "E:\pravoslavie_portal"

echo 📋 Выполняем действия для исправления админки...
echo.

echo 1️⃣ Останавливаем текущий сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak > nul

echo 2️⃣ Проводим диагностику админки...
python diagnose_admin.py
echo.

echo 3️⃣ Очищаем кеш Django...
python manage.py clear_cache 2>nul
echo.

echo 4️⃣ Проверяем миграции...
python manage.py migrate --check
echo.

echo 5️⃣ Собираем статические файлы...
python manage.py collectstatic --noinput --clear
echo.

echo 6️⃣ Запускаем сервер с исправлениями...
echo.
echo 🚀 Сервер будет доступен по адресу: http://127.0.0.1:8000/admin/
echo 📝 Попробуйте снова зайти в админку после запуска
echo.
echo ✅ Если проблема повторится:
echo    - Очистите кеш браузера (Ctrl+Shift+Delete)
echo    - Откройте админку в приватном режиме браузера
echo    - Проверьте консоль браузера на ошибки JavaScript
echo.

start "Django Server" python manage.py runserver 127.0.0.1:8000
echo.
echo 🔄 Сервер запущен в отдельном окне
echo 💡 Подождите 10 секунд и попробуйте зайти в админку
echo.

pause
