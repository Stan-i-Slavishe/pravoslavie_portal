@echo off
chcp 65001 >nul
echo 📜 ПРОСМОТР КОММИТОВ ПРОЕКТА
echo ============================

echo.
echo 🔍 Выберите способ просмотра коммитов:
echo.
echo 1. Все коммиты (подробно)
echo 2. Краткий список коммитов
echo 3. Последние 10 коммитов
echo 4. Графическое представление
echo 5. Коммиты за последнюю неделю
echo 6. Поиск по слову "комментарии"
echo 7. Поиск по слову "CSS"
echo 8. Изменения в main.css
echo 9. Статус репозитория
echo 0. Выход
echo.

set /p choice="Введите номер (0-9): "

if "%choice%"=="1" (
    echo.
    echo 📜 Все коммиты (подробно):
    echo =============================
    git log
    goto end
)

if "%choice%"=="2" (
    echo.
    echo 📋 Краткий список коммитов:
    echo ===========================
    git log --oneline -20
    goto end
)

if "%choice%"=="3" (
    echo.
    echo 🔟 Последние 10 коммитов:
    echo =========================
    git log --oneline -10 --graph
    goto end
)

if "%choice%"=="4" (
    echo.
    echo 🌳 Графическое представление:
    echo =============================
    git log --graph --oneline --all -15
    goto end
)

if "%choice%"=="5" (
    echo.
    echo 📅 Коммиты за последнюю неделю:
    echo ===============================
    git log --since="1 week ago" --oneline
    goto end
)

if "%choice%"=="6" (
    echo.
    echo 🔎 Поиск коммитов со словом "комментарии":
    echo ==========================================
    git log --grep="комментарии" --oneline
    git log --grep="comment" --oneline
    goto end
)

if "%choice%"=="7" (
    echo.
    echo 🎨 Поиск коммитов со словом "CSS":
    echo ==================================
    git log --grep="CSS" --oneline
    git log --grep="стили" --oneline
    goto end
)

if "%choice%"=="8" (
    echo.
    echo 📁 Изменения в main.css:
    echo ========================
    git log --oneline -- static/css/main.css
    goto end
)

if "%choice%"=="9" (
    echo.
    echo 📊 Статус репозитория:
    echo =====================
    git status
    echo.
    echo 📋 Последние 5 коммитов:
    echo =======================
    git log --oneline -5
    goto end
)

if "%choice%"=="0" (
    echo Выход...
    goto end
)

echo Неверный выбор!

:end
echo.
echo ============================
echo 💡 Полезные команды Git:
echo    git log --oneline       - краткий список
echo    git log --graph         - с графикой
echo    git log -n 10          - последние 10
echo    git status             - текущий статус
echo    git show [commit-hash] - детали коммита
echo ============================
pause
