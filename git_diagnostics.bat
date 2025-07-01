@echo off
echo ===== ДИАГНОСТИКА И ИСПРАВЛЕНИЕ GIT =====
echo.

echo 1. Проверяем конфигурацию Git...
git config --list | findstr user
echo.

echo 2. Проверяем статус репозитория...
git status
echo.

echo 3. Проверяем удаленные репозитории...
git remote -v
echo.

echo 4. Размер репозитория:
du -sh .git 2>nul || echo "Размер .git папки недоступен"
echo.

echo 5. Файлы, которые должны быть проигнорированы, но отслеживаются:
git ls-files -i -c --exclude-standard
echo.

echo 6. Большие файлы в репозитории:
git ls-files | xargs ls -la 2>nul | sort -k5 -n | tail -10
echo.

echo Возможные проблемы и решения:
echo.
echo "Если файлы не коммитятся:"
echo "- Проверьте .gitignore"
echo "- Используйте git add . для добавления всех файлов"
echo "- Проверьте права доступа к файлам"
echo.
echo "Если коммиты не видны:"
echo "- git log --all --graph --oneline"
echo "- Проверьте, на правильной ли вы ветке"
echo.
echo "Для принудительного добавления файлов:"
echo "- git add --force <file>"
echo.

pause
