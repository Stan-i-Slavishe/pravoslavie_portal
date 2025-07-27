@echo off
cd /d "E:\pravoslavie_portal"

echo ========================================
echo   ФИНАЛЬНЫЙ ТЕСТ PDF ЧИТАЛКИ 
echo ========================================
echo.

echo ✅ ВСЕ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ:
echo    - Инициализация canvas после загрузки DOM
echo    - Исправлена ошибка "Assignment to constant variable"
echo    - Улучшена обработка ошибок рендеринга
echo    - Добавлено подробное логирование
echo    - Исправлены CSRF ошибки
echo.

echo 🚀 Запуск сервера...
echo.
echo ОТКРОЙТЕ В БРАУЗЕРЕ:
echo 📖 http://127.0.0.1:8000/books/read/yandeks-direkt/
echo.
echo 🔍 ЧТО ПРОВЕРИТЬ В КОНСОЛИ БРАУЗЕРА:
echo    ✅ "PDF успешно загружен: N страниц"
echo    ✅ "Отображаем страницу 1 из N"
echo    ✅ "Страница 1 успешно отображена"
echo    ✅ "Прогресс сохранен: страница N"
echo.
echo ❌ ЕСЛИ НЕ РАБОТАЕТ, смотрите на ошибки:
echo    - "PDF документ не загружен"
echo    - "Canvas не инициализирован"
echo    - "Ошибка рендеринга страницы"
echo.

python manage.py runserver 127.0.0.1:8000
pause
