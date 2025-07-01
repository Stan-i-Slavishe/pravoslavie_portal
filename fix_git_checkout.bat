@echo off
chcp 65001 >nul
echo 🔄 РЕШЕНИЕ КОНФЛИКТА GIT CHECKOUT
echo =================================

echo ⚠️  Git не может переключиться из-за несохраненных изменений
echo 📁 Файл: static/css/stories.css
echo.

echo 💡 Выберите действие:
echo.
echo 1. 💾 Сохранить изменения в stash (рекомендуется)
echo 2. 🗑️ Удалить изменения и переключиться
echo 3. 📝 Создать коммит изменений
echo 4. ⚡ Принудительный откат (удалит ВСЕ изменения)
echo 5. 📊 Показать что изменилось
echo.

set /p choice="Выберите вариант (1-5): "

if "%choice%"=="1" (
    echo.
    echo 💾 Сохраняем изменения в stash...
    git stash push -m "Сохранение перед откатом к 82c2115"
    echo ✅ Изменения сохранены в stash
    echo.
    echo 🔄 Переключаемся на коммит 82c2115...
    git checkout 82c2115
    echo.
    echo 💡 Чтобы вернуть изменения позже: git stash pop
)

if "%choice%"=="2" (
    echo.
    echo 🗑️ Удаляем изменения в static/css/stories.css...
    git checkout -- static/css/stories.css
    echo ✅ Изменения удалены
    echo.
    echo 🔄 Переключаемся на коммит 82c2115...
    git checkout 82c2115
)

if "%choice%"=="3" (
    echo.
    echo 📝 Создаем коммит изменений...
    git add static/css/stories.css
    git commit -m "Сохранение CSS изменений перед откатом"
    echo ✅ Коммит создан
    echo.
    echo 🔄 Переключаемся на коммит 82c2115...
    git checkout 82c2115
)

if "%choice%"=="4" (
    echo.
    echo ⚠️  ВНИМАНИЕ: Это удалит ВСЕ несохраненные изменения!
    set /p confirm="Точно продолжить? (y/N): "
    if /i "!confirm!"=="y" (
        echo ⚡ Принудительный откат...
        git reset --hard 82c2115
        echo ✅ Откат выполнен
    ) else (
        echo ❌ Отменено
    )
)

if "%choice%"=="5" (
    echo.
    echo 📊 Что изменилось в static/css/stories.css:
    git diff static/css/stories.css
    echo.
    echo 📋 Общий статус:
    git status
)

echo.
echo 🔧 Применяем изменения...
python manage.py collectstatic --noinput

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo ✅ Готово! Откройте http://127.0.0.1:8000/stories/malishka/
pause
