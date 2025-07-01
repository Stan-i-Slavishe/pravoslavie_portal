@echo off
chcp 65001 >nul
echo 📜 ИСТОРИЯ КОММИТОВ GIT
echo =======================

echo 🔍 Последние 10 коммитов:
echo.
git log --oneline -10

echo.
echo 📊 Статус репозитория:
git status --short

echo.
echo 🌳 Ветки:
git branch -v

echo.
echo ====================================
echo 💡 Команды для отката:
echo.
echo 🔄 Мягкий откат (сохранить изменения):
echo    git reset --soft HEAD~1
echo.
echo ⚡ Жесткий откат (удалить изменения):
echo    git reset --hard HEAD~1
echo.
echo 🎯 Откат к конкретному коммиту:
echo    git reset --hard [hash коммита]
echo.
echo 📝 Создать новый коммит с откатом:
echo    git revert HEAD
echo ====================================
pause
