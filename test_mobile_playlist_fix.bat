@echo off
echo =================================
echo 🔧 ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЯ МОБИЛЬНОЙ ВЕРСИИ ПЛЕЙЛИСТА
echo =================================
echo.

echo ✅ Исправления применены:
echo    - flex-direction: column для .playlist-meta в мобильной версии
echo    - Уменьшенные отступы gap: 8px
echo    - Центрирование элементов align-items: center
echo    - Адаптивные размеры шрифтов и иконок
echo    - Правильное отображение кнопок действий
echo.

echo 📱 Проверьте страницу плейлиста в Chrome DevTools:
echo    1. Откройте F12 (Developer Tools)
echo    2. Включите Device Toggle (Ctrl+Shift+M)
echo    3. Выберите iPhone SE или другое мобильное устройство
echo    4. Перейдите на страницу плейлиста
echo.

echo 🎯 Что должно быть исправлено:
echo    - Метаданные НЕ должны накладываться друг на друга
echo    - Каждый элемент (количество рассказов, дата, статус) на отдельной строке
echo    - Все элементы центрированы
echo    - Кнопки действий располагаются вертикально
echo.

echo 🚀 Запускаем тестовый сервер...
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    python manage.py runserver 127.0.0.1:8000
) else (
    echo ❌ Виртуальное окружение не найдено!
    echo Убедитесь, что .venv существует
    pause
)
