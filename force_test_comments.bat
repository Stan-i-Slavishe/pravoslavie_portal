@echo off
chcp 65001 >nul
echo 🧪 ПРИНУДИТЕЛЬНЫЙ ТЕСТ СТАТИСТИКИ КОММЕНТАРИЕВ
echo ============================================

echo 🔧 Применяем принудительные стили...
python manage.py collectstatic --noinput --clear

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo 🎯 ТЕСТ ЗАПУЩЕН!
echo.
echo 📍 Что должно произойти:
echo    1. Блок метаданных станет ЖЕЛТЫМ с красной рамкой
echo    2. 4-й элемент (комментарии) станет ЗЕЛЕНЫМ с синей рамкой
echo    3. Текст комментариев будет виден принудительно
echo.
echo 🔍 Откройте: http://127.0.0.1:8000/stories/malishka/
echo.
echo 💡 Если НЕ видите цветные блоки:
echo    1. Очистите кеш браузера (Ctrl+Shift+R)
echo    2. Проверьте консоль F12 на ошибки
echo    3. Убедитесь, что CSS файл загружается
echo.
echo 📝 Если видите цветные блоки, но нет текста комментариев:
echo    - Проблема в передаче данных из view
echo    - Проверьте отладочный комментарий в исходном коде
echo.
pause
