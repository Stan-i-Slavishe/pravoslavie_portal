@echo off
echo ========================================
echo   ИСПРАВЛЕНИЕ ПРАВИЛЬНОГО ШАБЛОНА
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

echo ✅ Правильный шаблон исправлен!
echo.
echo 📋 Что было исправлено в templates/stories/story_detail.html:
echo    ✓ Уменьшен отступ с mb-4 на mb-2 (расстояние до комментариев)
echo    ✓ Упрощен блок поделиться - убран заголовок и описание
echo    ✓ Изменен отступ блока поделиться с mt-3 на mt-2
echo    ✓ Сделаны компактные кнопки btn-sm
echo    ✓ Кнопки WhatsApp и Telegram в горизонтальной строке
echo    ✓ Добавлен правильный URL encoding для ссылок
echo.
echo 🔄 Перезагрузите страницу в браузере (Ctrl+F5)
echo 🌐 http://127.0.0.1:8000/stories/malyshka/
echo.

pause
