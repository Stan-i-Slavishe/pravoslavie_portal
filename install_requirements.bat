@echo off
echo 🔧 Установка зависимостей для Православного портала...
echo.

REM Активация виртуального окружения
echo 📦 Активация виртуального окружения...
call .venv\Scripts\activate.bat

REM Обновление pip
echo 🔄 Обновление pip...
python -m pip install --upgrade pip

REM Установка всех зависимостей
echo 📚 Установка зависимостей из requirements.txt...
pip install -r requirements.txt

echo.
echo ✅ Установка завершена!
echo 🚀 Теперь можно запускать сервер: python manage.py runserver
echo.
pause
