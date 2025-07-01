@echo off
echo ===== БЫСТРЫЙ КОММИТ ВСЕХ ИЗМЕНЕНИЙ =====
echo.

echo Добавляем все файлы в staging...
git add .

echo.
echo Статус после добавления:
git status --short

echo.
set /p commit_message="Введите сообщение коммита (или нажмите Enter для автосообщения): "

if "%commit_message%"=="" (
    set commit_message=Автоматический коммит изменений %date% %time%
)

echo.
echo Выполняем коммит с сообщением: "%commit_message%"
git commit -m "%commit_message%"

echo.
echo Результат:
git log --oneline -5

echo.
echo Хотите запушить изменения? (y/n)
set /p push_choice=
if /i "%push_choice%"=="y" (
    echo Пушим изменения...
    git push
    echo Готово!
) else (
    echo Коммит выполнен, но не запушен.
)

pause
