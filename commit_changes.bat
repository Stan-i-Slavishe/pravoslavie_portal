@echo off
REM Скрипт для коммита всех изменений
REM commit_changes.bat

echo 📦 Сохранение всех изменений в Git...

git add .
git status

echo.
echo Файлы для коммита:
git diff --cached --name-only

echo.
set /p REPLY="Продолжить коммит? (y/n): "
if /i "%REPLY%"=="y" (
    git commit -m "Исправления для стабильной работы локального и продакшен окружений - Добавлен core/context_processors.py - Созданы отдельные настройки для окружений (local/production) - Исправлены проблемы с Django Debug Toolbar - Упрощены URL для стабильности - Добавлены скрипты автоматического запуска - Исправлена работа PWA и статических файлов"
    
    echo ✅ Изменения сохранены в Git
    echo 📤 Отправка на GitHub...
    git push origin main
    echo ✅ Изменения отправлены на сервер
) else (
    echo ❌ Коммит отменен
)

pause
