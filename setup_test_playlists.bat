@echo off
echo ===================================
echo СОЗДАНИЕ ТЕСТОВЫХ ПЛЕЙЛИСТОВ
echo ===================================
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
    echo Активация виртуального окружения...
    call .venv\Scripts\activate.bat
) else (
    echo Виртуальное окружение не найдено!
    echo Убедитесь что .venv существует
    pause
    exit /b 1
)

echo.
echo Создание тестовых плейлистов...
python create_test_playlists.py

echo.
echo ===================================
echo ГОТОВО!
echo ===================================
echo.
echo Теперь запустите сервер:
echo python manage.py runserver
echo.
echo И перейдите по ссылке:
echo http://127.0.0.1:8000/stories/playlists/
echo.
pause
