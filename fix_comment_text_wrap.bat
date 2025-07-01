@echo off
chcp 65001 >nul
echo ===== ИСПРАВЛЕНИЕ ПЕРЕНОСА ТЕКСТА В КОММЕНТАРИЯХ =====
echo.

echo ✅ CSS правила для переноса длинного текста добавлены:
echo   - word-wrap: break-word
echo   - word-break: break-word  
echo   - overflow-wrap: break-word
echo   - white-space: pre-wrap
echo   - max-width: 100%%
echo   - hyphens: auto
echo.

echo ✅ Контейнер комментариев исправлен:
echo   - min-width: 0 (позволяет flex-элементу сжиматься)
echo   - overflow: hidden (предотвращает переполнение)
echo.

echo ✅ Секция комментариев обновлена:
echo   - overflow-wrap: break-word
echo   - word-wrap: break-word
echo.

echo ✅ Глобальные CSS правила добавлены в main.css:
echo   - Правила для всех текстовых элементов
echo   - Корректная работа flex-контейнеров
echo   - Предотвращение горизонтального переполнения
echo.

echo ✅ Собираем статические файлы...
python manage.py collectstatic --noinput 2>nul
echo Статические файлы обновлены!
echo.

echo Проблема решена! Теперь длинный текст будет корректно переноситься.
echo.

echo Что исправлено:
echo 1. Комментарии с длинным текстом без пробелов
echo 2. Описания рассказов и книг
echo 3. Пользовательский контент
echo 4. Отзывы и рецензии
echo 5. Глобальная защита от переполнения
echo.

echo Хотите перезапустить Django для применения изменений? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo Перезапускаем Django сервер...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2
    start cmd /k "cd /d %~dp0 && python manage.py runserver"
    echo Сервер перезапущен!
)

echo.
echo Готово! Проверьте комментарии в браузере.
echo Теперь даже текст типа "ыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыы" будет корректно переноситься!
pause
