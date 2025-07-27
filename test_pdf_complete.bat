@echo off
cd /d "E:\pravoslavie_portal"

echo ========================================
echo   ПОЛНЫЙ ТЕСТ PDF ЧИТАЛКИ 
echo ========================================
echo.

echo 1. Проверяем текущее состояние книги...
python check_book_file.py
echo.

echo 2. Создаем тестовый PDF если нужно...
python create_test_pdf.py
echo.

echo 3. Проверяем после создания...
python check_book_file.py
echo.

echo 4. Запускаем сервер для тестирования...
echo.
echo ОТКРОЙТЕ В БРАУЗЕРЕ ОДНУ ИЗ ССЫЛОК:
echo.
echo ✅ Страница книги:
echo    http://127.0.0.1:8000/books/book/yandeks-direkt/
echo.
echo ✅ PDF читалка напрямую:
echo    http://127.0.0.1:8000/books/read/yandeks-direkt/
echo.
echo ✅ Файл PDF напрямую:
echo    http://127.0.0.1:8000/media/books/files/test_yandeks_direkt.pdf
echo.
echo Нажмите Ctrl+C для остановки сервера
echo ========================================
echo.

python manage.py runserver 127.0.0.1:8000
pause
