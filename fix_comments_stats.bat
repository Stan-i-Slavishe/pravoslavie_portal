@echo off
chcp 65001 >nul
echo 🔧 ПРИМЕНЕНИЕ ИСПРАВЛЕНИЙ СТАТИСТИКИ КОММЕНТАРИЕВ
echo ================================================

echo ✅ Исправления:
echo    1. Добавлен блок статистики комментариев в meta-item
echo    2. Добавлена отладочная информация
echo    3. Обновлена боковая панель с тремя колонками
echo    4. Добавлены CSS стили для адаптивности
echo.

echo 🔄 Очищаем кеш статических файлов...
python manage.py collectstatic --noinput --clear

echo 🗃️ Проверяем миграции...
python manage.py makemigrations
python manage.py migrate

echo 🚀 Перезапускаем сервер разработки...
taskkill /f /im python.exe 2>nul
timeout /t 3 /nobreak >nul

echo 🌐 Запускаем сервер...
start python manage.py runserver

echo.
echo 🎯 ГОТОВО! Проверьте результат:
echo.
echo 📍 Откройте: http://127.0.0.1:8000/stories/malishka/
echo 📝 Должно появиться: "💬 0 комментариев" рядом с лайками
echo 📊 В боковой панели: 3 колонки (Просмотры | Лайки | Комментарии)
echo.
echo 🐛 Если не работает:
echo    - Обновите страницу Ctrl+F5
echo    - Проверьте консоль браузера F12
echo    - Посмотрите исходный код страницы (отладочный комментарий)
echo.
pause
