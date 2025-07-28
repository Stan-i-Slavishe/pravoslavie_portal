@echo off
echo ============================================
echo   ИСПРАВЛЕНИЕ PDF READER - МАСШТАБИРОВАНИЕ
echo ============================================
echo.

echo 1. Создаем резервную копию старого файла...
copy "static\js\modern-reader.js" "static\js\modern-reader-backup.js"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)
echo ✓ Резервная копия создана: modern-reader-backup.js

echo.
echo 2. Заменяем файл на исправленную версию...
copy "static\js\modern-reader-fixed.js" "static\js\modern-reader.js"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось заменить файл!
    pause
    exit /b 1
)
echo ✓ Файл заменен на исправленную версию

echo.
echo 3. Удаляем временный файл...
del "static\js\modern-reader-fixed.js"
echo ✓ Временный файл удален

echo.
echo ============================================
echo   ИСПРАВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!
echo ============================================
echo.
echo Что было исправлено:
echo - Переименована переменная scale в userScale
echo - Исправлена функция renderPage()
echo - Исправлен обработчик слайдера масштаба
echo - Исправлено сохранение и загрузка настроек
echo.
echo Теперь масштабирование в PDF Reader работает правильно!
echo.
echo Нажмите любую клавишу для завершения...
pause >nul
