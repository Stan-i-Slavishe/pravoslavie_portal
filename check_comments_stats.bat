@echo off
chcp 65001 >nul
echo 🔍 ПРОВЕРКА СТАТИСТИКИ КОММЕНТАРИЕВ
echo ==================================

echo 📋 Проверяем, что блок комментариев добавлен в шаблон...
findstr /C:"comments-count-meta" "templates\stories\story_detail.html" >nul
if %errorlevel%==0 (
    echo ✅ Блок счетчика комментариев найден в шаблоне
) else (
    echo ❌ Блок счетчика комментариев НЕ найден в шаблоне
)

echo.
echo 📋 Проверяем контекст в views.py...
findstr /C:"comments_count" "stories\views.py" >nul
if %errorlevel%==0 (
    echo ✅ comments_count передается в контексте
) else (
    echo ❌ comments_count НЕ найден в views.py
)

echo.
echo 🎨 Проверяем CSS стили...
findstr /C:"comments-count-sidebar" "static\css\stories.css" >nul
if %errorlevel%==0 (
    echo ✅ CSS стили для статистики найдены
) else (
    echo ❌ CSS стили НЕ найдены
)

echo.
echo 🔧 Применяем изменения и перезапускаем...
python manage.py collectstatic --noinput --clear
echo ✅ Статические файлы обновлены

echo.
echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo 💡 Если счетчик все еще не виден:
echo    1. Убедитесь, что сервер перезапустился
echo    2. Обновите страницу в браузере (Ctrl+F5)
echo    3. Проверьте консоль браузера на ошибки
echo    4. Убедитесь, что у рассказа есть комментарии
echo.
echo 🌐 Откройте: http://127.0.0.1:8000/stories/malishka/
pause
