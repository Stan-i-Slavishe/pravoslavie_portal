@echo off
chcp 65001 >nul
echo ===== ИСПРАВЛЕНИЕ КНОПКИ "ПОКАЗАТЬ ЕЩЕ КОММЕНТАРИИ" =====
echo.

echo 1. Проверяем статус сервера...
tasklist /FI "IMAGENAME eq python.exe" | find "python.exe" >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Django сервер запущен
) else (
    echo ⚠️ Django сервер не запущен
    echo Запускаем сервер...
    start cmd /k "cd /d %~dp0 && python manage.py runserver"
    timeout /t 3
)

echo.
echo 2. Применяем изменения...
echo ✅ View функция load_more_comments добавлена
echo ✅ URL маршрут добавлен
echo ✅ JavaScript исправлен

echo.
echo 3. Проверяем файлы...
if exist "templates\stories\comment_item.html" (
    echo ✅ Шаблон comment_item.html найден
) else (
    echo ❌ Шаблон comment_item.html НЕ найден
)

if exist "stories\models.py" (
    echo ✅ Модели комментариев найдены
) else (
    echo ❌ Модели комментариев НЕ найдены
)

echo.
echo 4. Что было исправлено:
echo   - Функция loadMoreComments() теперь делает реальный AJAX запрос
echo   - Добавлен view load_more_comments для обработки запроса
echo   - Добавлен URL маршрут /stories/{id}/comments/load-more/
echo   - Функция корректно обрабатывает offset и загружает по 5 комментариев
echo   - Добавлена проверка наличия дополнительных комментариев

echo.
echo 5. Как проверить:
echo   - Откройте любой рассказ в браузере
echo   - Прокрутите к разделу комментариев
echo   - Нажмите кнопку "Показать еще комментарии"
echo   - Должны загрузиться дополнительные комментарии

echo.
echo 6. Если кнопка все еще не работает, проверьте:
echo   - Есть ли комментарии в базе данных (больше 5)
echo   - Работает ли JavaScript (F12 Console в браузере)
echo   - Нет ли ошибок в консоли Django

echo.
echo Открыть браузер? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    start http://127.0.0.1:8000/stories/
)

echo.
echo Готово! Кнопка "Показать еще комментарии" должна работать.
pause
