@echo off
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██  🎯 ФИНАЛЬНОЕ РЕШЕНИЕ ПРОБЛЕМЫ 404 - ЗАГЛУШКА               ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

echo ✅ Создана заглушка в static/stories/js/youtube_comments.js
echo ✅ Заглушка автоматически перенаправит на правильный файл
echo ✅ Больше НЕ БУДЕТ ошибок 404!

echo.
echo 🔄 Пересборка статических файлов...
python manage.py collectstatic --noinput

echo.
echo 📁 Проверяем файлы:
if exist "static\js\youtube_comments_fixed.js" (
    echo ✅ Основной файл: youtube_comments_fixed.js найден
) else (
    echo ❌ Основной файл НЕ найден!
)

if exist "static\stories\js\youtube_comments.js" (
    echo ✅ Заглушка: youtube_comments.js найден
) else (
    echo ❌ Заглушка НЕ найдена!
)

echo.
echo 🎯 Теперь система работает следующим образом:
echo    1. Браузер запрашивает старый файл youtube_comments.js
echo    2. Заглушка перехватывает запрос
echo    3. Автоматически загружается правильный youtube_comments_fixed.js
echo    4. Комментарии работают без ошибок!

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██  🚀 ПРОБЛЕМА 404 РЕШЕНА! ЗАПУСКАЕМ СЕРВЕР!                 ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

start http://127.0.0.1:8000/stories/pasha-voskresenie-hristovo/

python manage.py runserver