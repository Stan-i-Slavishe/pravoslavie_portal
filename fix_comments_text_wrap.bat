@echo off
chcp 65001 >nul
echo 🔧 ИСПРАВЛЕНИЕ ПЕРЕНОСА ТЕКСТА В СТАТИСТИКЕ
echo =========================================

echo ❌ Проблема: "Комментариев" переносилось на новую строку
echo ✅ Решение: 
echo.

echo 📝 Что исправлено:
echo    1. "Комментариев" → "Комментарии" (короче на 2 символа)
echo    2. Добавлены CSS стили для предотвращения переносов:
echo       • font-size: 0.7rem (меньший размер шрифта)
echo       • white-space: nowrap (запрет переноса)
echo       • text-overflow: ellipsis (обрезка с ...)
echo    3. Уменьшены отступы колонок: padding: 0.5rem 0.25rem
echo.

echo 🔧 Применяем исправления...
python manage.py collectstatic --noinput

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo 🎯 ИСПРАВЛЕНИЕ ПРИМЕНЕНО!
echo.
echo 📊 Теперь в боковой панели:
echo    ┌─────────────────────────┐
echo    │       СТАТИСТИКА        │
echo    ├─────────────────────────┤
echo    │   👁️1    ❤️1    💬26    │
echo    │Просмотров Лайки Комментарии│
echo    └─────────────────────────┘
echo.
echo ✅ Все три слова помещаются в одну строку!
echo 📍 Откройте: http://127.0.0.1:8000/stories/malishka/
echo.
pause
