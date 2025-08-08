@echo off
echo 🖼️ Добавляем поддержку превью изображений для видео...
echo.

cd /d "E:\pravoslavie_portal"

echo 📝 Создаем миграцию для добавления поля thumbnail...
python manage.py makemigrations stories

echo.
echo 🚀 Применяем миграцию...
python manage.py migrate

echo.
echo ✅ Поле thumbnail добавлено к модели Story!
echo.
echo 🎯 Теперь:
echo 1. В админке Stories можно загружать превью изображения
echo 2. Если превью не загружено, будет использоваться превью с YouTube
echo 3. Страница тегов теперь будет показывать превью видео!
echo.
echo 📋 Превью с YouTube генерируется автоматически по формуле:
echo https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg
echo.
pause
