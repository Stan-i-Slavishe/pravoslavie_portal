@echo off
chcp 65001 >nul
echo ⚡ БЫСТРОЕ ТЕСТИРОВАНИЕ ПРИНУДИТЕЛЬНЫХ СТИЛЕЙ
echo ============================================

echo 🔧 Обновляем статические файлы...
python manage.py collectstatic --noinput --clear

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 3 /nobreak >nul
start python manage.py runserver

echo.
echo 🎯 ПРИНУДИТЕЛЬНЫЙ ТЕСТ АКТИВИРОВАН!
echo.
echo 📍 Откройте: http://127.0.0.1:8000/stories/malishka/
echo.
echo 🔍 ДОЛЖНО ПОЯВИТЬСЯ:
echo    🟨 ЖЕЛТЫЙ блок с красной рамкой
echo    🟩 ЗЕЛЕНЫЕ элементы с синей рамкой внутри
echo    📝 Черный текст: дата, просмотры, лайки, TEST-0 комментариев
echo.
echo ❌ Если НЕ видите цветные блоки:
echo    - Элементы полностью отсутствуют
echo    - CSS не загружается
echo    - Серьезная проблема с шаблоном
echo.
echo ✅ Если видите цветные блоки:
echo    - Элементы есть, просто были скрыты CSS
echo    - Можно убрать диагностические стили
echo    - Найти и исправить конфликтующий CSS
echo.
pause
