@echo off
echo =================================
echo 🎯 ТЕСТИРОВАНИЕ GRID ИСПРАВЛЕНИЯ ПЛЕЙЛИСТОВ
echo =================================
echo.

echo ✅ Применен CSS Grid подход:
echo    - grid-template-columns: 1fr 1fr (две равные колонки)
echo    - grid-template-rows: auto auto (две строки)
echo    - Элемент 3 (статус): grid-column: 1 / -1, grid-row: 1
echo    - Элемент 1 (количество): grid-column: 1, grid-row: 2
echo    - Элемент 2 (дата): grid-column: 2, grid-row: 2
echo.

echo 📱 Ожидаемый результат:
echo    ┌─────────────────────────────────┐
echo    │        🔒 Приватный             │  ← Строка 1 (колонки 1-2)
echo    ├─────────────┬───────────────────┤
echo    │ 📚 3 рассказа │ 📅 12 Июль 2025  │  ← Строка 2 (колонка 1 + 2)
echo    └─────────────┴───────────────────┘
echo.

echo 🛠️ Технические детали:
echo    - CSS Grid обеспечивает точное позиционирование
echo    - !important для переопределения inline стилей
echo    - Файл: static/css/azbyka-style.css
echo.

echo 🧪 Проверка:
echo    1. Очистите кеш браузера (Ctrl+Shift+R)
echo    2. F12 -> Device Toggle -> iPhone SE
echo    3. Проверьте плейлист на корректное отображение
echo.

echo 🚀 Запускаем тестовый сервер...
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    python manage.py runserver 127.0.0.1:8000 --insecure
) else (
    echo ❌ Виртуальное окружение не найдено!
    pause
)
