@echo off
echo 🎯 Диагностика центрирования иконки воспроизведения
echo.

REM Активация виртуального окружения
echo 📦 Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo.
echo 🚀 Запуск сервера для диагностики...
echo.
echo 🔍 Что проверить в Dev Tools:
echo.
echo 1. Откройте Developer Tools (F12)
echo 2. Включите Device Mode (Ctrl+Shift+M)
echo 3. Выберите iPhone/Android устройство
echo 4. Правой кнопкой на иконку ▶️ → "Inspect"
echo.
echo 📋 Параметры для проверки:
echo.
echo ✅ .playlist-play-icon должна иметь:
echo    • position: absolute
echo    • top: 50%%
echo    • left: 50%%
echo    • transform: translate(-50%%, -50%%)
echo    • z-index: 10
echo.
echo ✅ .playlist-thumbnail должна иметь:
echo    • position: relative
echo    • width: 100%%
echo    • height: 200px
echo.
echo 🎯 Ожидаемое расположение:
echo    Иконка должна быть точно по центру превью,
echo    не смещена ни влево, ни вправо, ни вверх, ни вниз
echo.
echo 💡 Если иконка не по центру:
echo    Проверьте наличие других элементов с position absolute
echo    в том же контейнере, которые могут влиять на positioning context
echo.
echo 🌐 Откройте: http://127.0.0.1:8000/stories/playlists/
echo.
python manage.py runserver
