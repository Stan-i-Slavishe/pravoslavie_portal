@echo off
chcp 65001 >nul
echo 🔍 ПРИНУДИТЕЛЬНОЕ ОБНОВЛЕНИЕ СТАТИСТИКИ КОММЕНТАРИЕВ
echo =================================================

echo ✅ Изменения применены:
echo    1. Обновлен templates/stories/detail_v2.html
echo    2. Добавлен блок комментариев в метаданные
echo    3. Обновлена боковая панель (3 колонки)
echo    4. Добавлена тестовая переменная TEST-0
echo    5. Добавлен отладочный комментарий
echo.

echo 🔧 Принудительное обновление...
python manage.py collectstatic --noinput --clear

echo 🗑️ Очищаем кеш Django...
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Кеш очищен')"

echo 🚀 Принудительный перезапуск сервера...
taskkill /f /im python.exe 2>nul
timeout /t 3 /nobreak >nul

echo ✨ Запускаем сервер заново...
start python manage.py runserver

echo.
echo 🎯 ОБНОВЛЕНИЯ ПРИМЕНЕНЫ!
echo.
echo 📍 Теперь должно появиться:
echo    ✅ "💬 TEST-0 комментариев" в метаданных
echo    ✅ Третья колонка "TEST-0" в боковой панели
echo    ✅ Отладочный комментарий в исходном коде
echo.
echo 🔍 Проверьте:
echo    1. http://127.0.0.1:8000/stories/malishka/
echo    2. Обновите страницу Ctrl+F5
echo    3. Посмотрите исходный код (Ctrl+U)
echo    4. Найдите "<!-- Отладка: ... -->"
echo.
echo 💡 Если появился "TEST-0" - шаблон работает!
echo    Если "UNDEFINED" - проблема в передаче данных
pause
