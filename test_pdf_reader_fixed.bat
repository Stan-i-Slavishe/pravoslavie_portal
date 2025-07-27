@echo off
echo ========================================
echo    ТЕСТ PDF ЧИТАЛКИ - ИСПРАВЛЕННАЯ ВЕРСИЯ
echo ========================================
echo.

echo 1. Проверяем информацию о книге...
python check_book_file.py
echo.

echo 2. Запускаем сервер Django...
echo.
echo ОТКРОЙТЕ В БРАУЗЕРЕ:
echo http://127.0.0.1:8000/books/read/yandeks-direkt/
echo.
echo Нажмите Ctrl+C для остановки сервера
echo.

python manage.py runserver 127.0.0.1:8000
pause
