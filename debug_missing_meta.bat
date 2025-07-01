@echo off
chcp 65001 >nul
echo 🔍 ДИАГНОСТИКА ПРОПАВШЕЙ СТАТИСТИКИ
echo ===================================

echo 📊 Проблема: метаданные под заголовком не отображаются
echo 📍 Боковая панель видна, но основной блок .story-meta скрыт
echo.

echo 🔧 Применяем принудительные стили для диагностики...

echo /* ПРИНУДИТЕЛЬНОЕ ОТОБРАЖЕНИЕ МЕТАДАННЫХ */ > static\css\debug-meta.css
echo .story-meta { >> static\css\debug-meta.css
echo     display: flex !important; >> static\css\debug-meta.css
echo     visibility: visible !important; >> static\css\debug-meta.css
echo     background: yellow !important; >> static\css\debug-meta.css
echo     border: 3px solid red !important; >> static\css\debug-meta.css
echo     padding: 20px !important; >> static\css\debug-meta.css
echo     margin: 20px 0 !important; >> static\css\debug-meta.css
echo } >> static\css\debug-meta.css
echo. >> static\css\debug-meta.css
echo .meta-item { >> static\css\debug-meta.css
echo     display: flex !important; >> static\css\debug-meta.css
echo     background: lime !important; >> static\css\debug-meta.css
echo     border: 2px solid blue !important; >> static\css\debug-meta.css
echo     padding: 10px !important; >> static\css\debug-meta.css
echo     margin: 5px !important; >> static\css\debug-meta.css
echo     color: black !important; >> static\css\debug-meta.css
echo     font-size: 16px !important; >> static\css\debug-meta.css
echo } >> static\css\debug-meta.css

echo ✅ Создан debug-meta.css

echo 🔄 Обновляем статические файлы...
python manage.py collectstatic --noinput

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo 🎯 ДИАГНОСТИЧЕСКИЙ ТЕСТ ЗАПУЩЕН!
echo.
echo 📍 Откройте: http://127.0.0.1:8000/stories/malishka/
echo.
echo 🔍 Что должно произойти:
echo    ✅ Желтый блок с красной рамкой (story-meta)
echo    ✅ Зеленые блоки с синей рамкой (meta-item)
echo    ✅ Крупный черный текст метаданных
echo.
echo 💡 Если НЕ видите цветные блоки:
echo    - CSS файл не загружается
echo    - Элементы удалены другим CSS
echo    - Проблема с шаблоном
echo.
echo 💡 Если видите цветные блоки:
echo    - Элементы есть, но скрыты другими стилями
echo    - Нужно найти конфликтующий CSS
echo.
pause
