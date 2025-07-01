@echo off
echo ========================================
echo   ИСПРАВЛЕНИЕ ШАБЛОНОВ И ПРЕДСТАВЛЕНИЙ
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

echo ✅ Представления исправлены на правильный шаблон!
echo.
echo 📋 Что исправлено:
echo    ✓ StoryListView: stories/story_list.html → stories/list.html
echo    ✓ StoryCategoryView: stories/story_list.html → stories/list.html  
echo    ✓ StoryTagView: stories/story_list.html → stories/list.html
echo    ✓ PopularStoriesView: stories/story_list.html → stories/list.html
echo    ✓ FeaturedStoriesView: stories/story_list.html → stories/list.html
echo.
echo 📍 Теперь Django будет использовать правильный шаблон stories/list.html
echo    где уже есть метаданные комментариев:
echo    [👁️ просмотры] [💬 комментарии]
echo.
echo 🔄 Перезагрузите страницу в браузере (Ctrl+F5)
echo 🌐 http://127.0.0.1:8000/stories/
echo.

pause
