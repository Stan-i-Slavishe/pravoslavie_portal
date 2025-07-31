@echo off
echo ===============================================
echo 🔍 ДИАГНОСТИКА: Проверяем почему кнопка не появляется
echo ===============================================
echo.
echo 📋 Кнопка "Читать на весь экран" уже добавлена в шаблон!
echo    Файл: templates/books/book_detail.html
echo    Строки: 362-367
echo.
echo 🔍 Возможные причины почему кнопка не отображается:
echo    1. У книги нет файла (book.file пустое)
echo    2. Ошибка в URL маршруте books:modern_reader
echo    3. Условие {% if book.file %} не выполняется
echo.
echo 🚀 Запускаем сервер для диагностики...
echo    Откройте DevTools (F12) и проверьте консоль на ошибки
echo.

cd /d "E:\pravoslavie_portal"
python manage.py runserver 127.0.0.1:8000
