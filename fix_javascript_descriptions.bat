@echo off
echo 🔧 Исправление проблемы с JavaScript описаний
echo.
echo ✅ Проблема: Страница дозагружалась и возвращалась к полным описаниям
echo ✅ Решение: Улучшена логика определения коротких/длинных текстов
echo.

cd /d "E:\pravoslavie_portal"

echo ⏹️ Остановка сервера...
taskkill /f /im python.exe 2>nul

echo 🧹 Очистка кеша...
if exist "__pycache__" rmdir /s /q "__pycache__"

echo 🚀 Запуск сервера...
echo.
echo 💡 Что исправлено:
echo    - Добавлена задержка загрузки JavaScript (100ms)
echo    - Улучшена логика измерения высоты текста
echo    - Исправлено определение коротких описаний
echo    - Стабильное отображение 3 строк + кнопка
echo.
echo 📱 Откройте: http://127.0.0.1:8000/categories/
echo 👀 Проверьте: описания должны оставаться сокращенными
echo.

python manage.py runserver 127.0.0.1:8000

pause
