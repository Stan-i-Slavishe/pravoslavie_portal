@echo off
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██  🔍 ДЕТЕКТИВНАЯ РАБОТА - ИЩЕМ ИСТОЧНИК 404 ОШИБКИ          ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

echo 🔍 Ищем все упоминания youtube_comments.js в проекте...
echo.

echo 📁 Поиск в HTML шаблонах:
findstr /s /n /i "youtube_comments\.js" "*.html" 2>nul
findstr /s /n /i "youtube_comments\.js" "templates\*.html" 2>nul
findstr /s /n /i "youtube_comments\.js" "stories\templates\*.html" 2>nul

echo.
echo 📁 Поиск в JavaScript файлах:
findstr /s /n /i "youtube_comments\.js" "*.js" 2>nul
findstr /s /n /i "youtube_comments\.js" "static\*.js" 2>nul

echo.
echo 📁 Поиск в Python файлах:
findstr /s /n /i "youtube_comments\.js" "*.py" 2>nul

echo.
echo 🔍 Поиск по содержимому файлов:
echo.
echo === В story_detail.html ===
findstr /n "youtube_comments" "stories\templates\stories\story_detail.html" 2>nul
echo.
echo === В youtube_comments.html ===
findstr /n "youtube_comments" "stories\templates\stories\partials\youtube_comments.html" 2>nul

echo.
echo 🧹 Создаем временный файл для тестирования...
echo console.log('ФАЙЛ ЗАГРУЖЕН УСПЕШНО!'); > "static\stories\js\youtube_comments.js"

echo.
echo 📁 Проверяем структуру каталогов:
echo.
echo === static/js/ ===
dir "static\js\" 2>nul
echo.
echo === static/stories/js/ ===
dir "static\stories\js\" 2>nul

echo.
echo 🔄 Пересборка статических файлов...
python manage.py collectstatic --noinput

echo.
echo ✅ Диагностика завершена!
echo 📝 Проверьте вывод выше для поиска источника проблемы
echo.

pause