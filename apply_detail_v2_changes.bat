@echo off
echo ========================================
echo   ПРИМЕНЕНИЕ ИЗМЕНЕНИЙ К DETAIL_V2.HTML
echo ========================================
echo.

echo 🗂️ Переходим в директорию проекта...
cd /d "E:\pravoslavie_portal"

echo 🔧 Активируем виртуальное окружение...
call venv\Scripts\activate

echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

echo 🔄 Очищаем кэш Django...
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Кэш очищен!')"

echo ✅ Изменения применены к правильному шаблону!
echo.
echo 📋 Что было исправлено:
echo    ✓ Найден правильный шаблон: detail_v2.html
echo    ✓ Добавлены кнопки "Нравится" и "Поделиться" 
echo    ✓ Кнопки расположены горизонтально
echo    ✓ Добавлен JavaScript для функций
echo    ✓ Добавлен блок социальных кнопок
echo.
echo 🔄 Перезагрузите страницу в браузере (Ctrl+F5)
echo 🌐 http://127.0.0.1:8000/stories/malyshka/
echo.

pause
