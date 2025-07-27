@echo off
cd /d "E:\pravoslavie_portal"

echo ========================================
echo   ТЕСТ PDF ЧИТАЛКИ - ИСПРАВЛЕНИЯ CSRF
echo ========================================
echo.

echo ✅ Исправлены CSRF ошибки:
echo    - Улучшена функция getCookie
echo    - Добавлена функция getCSRFToken
echo    - Добавлен мета-тег с CSRF токеном
echo    - Улучшена обработка ошибок
echo.

echo 🚀 Запускаем сервер...
echo.
echo ТЕСТИРУЙТЕ:
echo 📖 http://127.0.0.1:8000/books/read/yandeks-direkt/
echo.
echo ✅ Что должно работать:
echo    - Загрузка PDF (уже работает)
echo    - Навигация по страницам
echo    - Сохранение прогресса БЕЗ ошибок CSRF
echo    - Добавление закладок
echo.
echo ❌ Если все еще есть ошибки CSRF:
echo    - Проверьте настройки CSRF в settings.py
echo    - Проверьте middleware
echo.

python manage.py runserver 127.0.0.1:8000
pause
