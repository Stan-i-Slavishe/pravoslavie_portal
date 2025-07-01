@echo off
chcp 65001 >nul
echo 📱 МОБИЛЬНАЯ АДАПТИВНОСТЬ КНОПОК
echo ================================

echo ✅ Что улучшено для мобильных:
echo.
echo 📍 Горизонтальное расположение кнопок:
echo    ✓ flex-direction: row (в строку, а не в столбец)
echo    ✓ gap: 0.75rem (уменьшенный отступ между кнопками)
echo    ✓ justify-content: center (по центру экрана)
echo.
echo 📍 Размеры кнопок:
echo    ✓ flex: 1 (равномерное заполнение ширины)
echo    ✓ max-width: 180px (максимальная ширина)
echo    ✓ font-size: 0.85rem (немного меньше текст)
echo    ✓ padding: 0.65rem 1rem (компактные отступы)
echo.
echo 📍 Выпадающее меню:
echo    ✓ right: 0 (прижато к правому краю)
echo    ✓ min-width: 180px (компактная ширина)
echo    ✓ Уменьшенные отступы и размеры текста
echo.

echo 🔧 Применяем мобильную адаптивность...
python manage.py collectstatic --noinput

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo 🎯 МОБИЛЬНАЯ АДАПТИВНОСТЬ ГОТОВА!
echo.
echo 📱 Результат на мобильных:
echo    ┌─────────────────────────────┐
echo    │  🔴 [❤️ Нравится]  🔵 [📤]  │
echo    │       (1)      Поделиться   │
echo    └─────────────────────────────┘
echo    ↑                           ↑
echo    Равномерно по ширине экрана
echo.
echo ✅ Преимущества:
echo    • Кнопки расположены горизонтально
echo    • Занимают всю ширину экрана
echo    • Удобно нажимать пальцем
echo    • Выпадающее меню адаптировано
echo.
echo 📍 Откройте на мобильном: http://127.0.0.1:8000/stories/malishka/
echo 💡 Или уменьшите ширину браузера для проверки
pause
