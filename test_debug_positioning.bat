@echo off
echo 🔧 Отладка позиционирования иконки с !important
echo.

REM Активация виртуального окружения
echo 📦 Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo.
echo 🚀 Запуск сервера с принудительным позиционированием...
echo.
echo 🔍 ИНСТРУКЦИЯ ПО ОТЛАДКЕ:
echo.
echo 1. Откройте Developer Tools (F12)
echo 2. Включите Device Mode (Ctrl+Shift+M)  
echo 3. Выберите iPhone или другое мобильное устройство
echo 4. Найдите иконку ▶️ на странице
echo 5. Правый клик на иконку → "Inspect Element"
echo.
echo 📋 В Dev Tools проверьте:
echo.
echo ✅ Убедитесь, что элемент имеет класс "playlist-play-icon"
echo ✅ Во вкладке "Computed" проверьте:
echo    • position: absolute
echo    • top: 50%%  
echo    • left: 50%%
echo    • transform: translate(-50%%, -50%%)
echo    • z-index: 15
echo.
echo 🎯 Если иконка все еще смещена:
echo    Посмотрите на родительские элементы (.youtube-thumbnail)
echo    и проверьте их position, width, height
echo.
echo 💡 Теперь используются !important правила,
echo    которые должны переопределить любые конфликтующие стили
echo.
echo 🌐 Откройте: http://127.0.0.1:8000/stories/playlists/
echo.
python manage.py runserver
