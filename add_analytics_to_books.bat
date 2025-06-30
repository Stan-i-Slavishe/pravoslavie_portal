@echo off
chcp 65001 >nul
echo Добавляем аналитику в библиотеку...

echo.
echo Удаляем старые статические файлы...
rmdir /s /q staticfiles 2>nul

echo.
echo Собираем новые статические файлы...
python manage.py collectstatic --noinput

echo.
echo Аналитика добавлена в библиотеку!
echo.
echo Что добавлено:
echo   - JavaScript обработчик кнопок с data-analytics-track
echo   - Виджет подписки на страницах книг
echo   - Красивый попап подписки после клика
echo   - Анимация пульсации для привлечения внимания
echo   - Сообщение "Интерес записан!" остается постоянно
echo.
echo Запустите сервер: python manage.py runserver
echo Очистите кеш браузера Ctrl+F5
pause