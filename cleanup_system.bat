@echo off
echo 🧹 Очистка системы Django проекта
echo.

REM Активируем виртуальное окружение
call .venv\Scripts\activate

REM Запускаем скрипт очистки
python optimize_performance.py

REM Очищаем пайкеш
echo 🗑️ Очистка __pycache__...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

REM Очищаем .pyc файлы
echo 🗑️ Очистка .pyc файлов...
del /s /q *.pyc

echo.
echo ✅ Очистка завершена!
pause
