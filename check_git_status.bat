@echo off
echo ===== ПРОВЕРКА СТАТУСА GIT =====
echo.

echo Текущая ветка:
git branch

echo.
echo Статус файлов:
git status

echo.
echo Файлы, не отслеживаемые Git:
git ls-files --others --exclude-standard

echo.
echo Последние 10 коммитов:
git log --oneline -10

echo.
echo Измененные файлы (не закоммиченные):
git diff --name-only

echo.
echo Файлы в staging area:
git diff --cached --name-only

pause
