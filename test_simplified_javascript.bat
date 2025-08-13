@echo off
echo 🔧 УПРОЩЕННАЯ ВЕРСИЯ JavaScript для кнопок
echo.
echo ✅ Что изменено:
echo    - Полностью переписан JavaScript более простым способом
echo    - Убраны сложные стрелочные функции
echo    - Убрана логика автоскрытия коротких описаний
echo    - Используются обычные function() вместо arrow functions
echo    - Увеличена задержка инициализации до 150ms
echo    - Добавлена подробная отладка каждого шага
echo.

cd /d "E:\pravoslavie_portal"

echo ⏹️ Остановка сервера...
taskkill /f /im python.exe 2>nul

echo 🧹 Очистка кеша...
if exist "__pycache__" rmdir /s /q "__pycache__"

echo 🚀 Запуск сервера...
echo.
echo 💡 Что делать для тестирования:
echo    1. Откройте http://127.0.0.1:8000/categories/
echo    2. Откройте DevTools (F12) → Console
echo    3. Должны увидеть подробные логи инициализации
echo    4. Кликните по любой кнопке "Показать всё"
echo    5. В консоли должно появиться "👆 КЛИК ПО КНОПКЕ!"
echo    6. Описание должно развернуться
echo.
echo 📋 Если НЕ работает - пришлите скриншот консоли!
echo.

python manage.py runserver 127.0.0.1:8000

pause
