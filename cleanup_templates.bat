@echo off
chcp 65001 >nul
echo 🧹 ОЧИСТКА И ФИНАЛЬНАЯ НАСТРОЙКА ШАБЛОНОВ
echo ==========================================

echo ✅ Что сделано:
echo    1. story_detail.html → story_detail.html.old (старый файл)
echo    2. detail_v2.html → story_detail.html (рабочий файл)
echo    3. Теперь view использует правильный шаблон
echo    4. Убрана путаница с дублированными файлами
echo.

echo 🔍 Проверяем структуру шаблонов...
echo.
echo 📁 Текущие файлы в templates/stories/:
dir /b "templates\stories\*.html" | findstr story_detail

echo.
echo 🔧 Применяем изменения...
python manage.py collectstatic --noinput --clear

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo 🎯 ФИНАЛЬНАЯ НАСТРОЙКА ЗАВЕРШЕНА!
echo.
echo ✅ Теперь используется единственный правильный шаблон:
echo    templates/stories/story_detail.html
echo.
echo 📍 Откройте: http://127.0.0.1:8000/stories/malishka/
echo 💬 Должно появиться: "TEST-0 комментариев"
echo.
echo 🗑️ Если все работает, можно удалить:
echo    - story_detail.html.old (старый файл)
echo    - другие backup файлы story_detail_*.html
echo.
pause
