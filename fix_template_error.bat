@echo off
echo ===============================
echo 🔧 ИСПРАВЛЕНИЕ ОШИБКИ ШАБЛОНА
echo ===============================
echo.

echo ✅ Ошибка в story_detail.html исправлена!
echo.
echo 📋 Что было исправлено:
echo - Убран лишний endblock на строке 34
echo - CSS стили обернуты в block extra_head
echo - Исправлен синтаксис Django шаблона
echo.

echo 🔍 Проверяем остальные шаблоны...
python check_template_syntax.py

echo.
echo 🚀 Перезапускаем сервер...
echo Нажмите Ctrl+C чтобы остановить сервер
echo.

python manage.py runserver
