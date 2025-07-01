@echo off
chcp 65001 >nul
echo 🚀 БЫСТРЫЙ ПРОСМОТР КОММИТОВ
echo ============================

echo 📊 Статус репозитория:
git status --short

echo.
echo 📋 Последние 15 коммитов:
echo ========================
git log --oneline --graph -15

echo.
echo 🔍 Поиск недавних изменений CSS:
echo ===============================
git log --grep="CSS" --grep="стили" --grep="компакт" --oneline -10

echo.
echo 📁 Последние изменения в статических файлах:
echo ============================================
git log --oneline -5 -- static/

echo.
echo ============================
echo 💡 Для детального просмотра:
echo    git show [hash] - детали коммита
echo    git log --stat  - с файлами
echo    view_commits.bat - полное меню
echo ============================
pause
