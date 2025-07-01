@echo off
echo ===== ВЫБОРОЧНЫЙ КОММИТ =====
echo.

echo Измененные файлы:
git status --porcelain

echo.
echo Выберите действие:
echo 1. Добавить конкретный файл
echo 2. Добавить все файлы определенного типа
echo 3. Добавить все Python файлы (.py)
echo 4. Добавить все HTML файлы (.html)
echo 5. Добавить все CSS/JS файлы
echo 6. Посмотреть изменения в файле
echo 7. Откатить изменения в файле
echo 8. Создать коммит из staging area
echo 9. Выход

set /p choice="Ваш выбор (1-9): "

if "%choice%"=="1" (
    set /p filename="Введите имя файла (с путем): "
    git add "%filename%"
    echo Файл %filename% добавлен в staging
)

if "%choice%"=="2" (
    set /p pattern="Введите маску файлов (например, *.py): "
    git add "%pattern%"
    echo Файлы %pattern% добавлены в staging
)

if "%choice%"=="3" (
    git add *.py
    echo Все Python файлы добавлены в staging
)

if "%choice%"=="4" (
    git add *.html templates/**/*.html
    echo Все HTML файлы добавлены в staging
)

if "%choice%"=="5" (
    git add *.css *.js static/**/*.css static/**/*.js
    echo Все CSS/JS файлы добавлены в staging
)

if "%choice%"=="6" (
    set /p filename="Введите имя файла для просмотра изменений: "
    git diff "%filename%"
)

if "%choice%"=="7" (
    set /p filename="Введите имя файла для отката: "
    git checkout -- "%filename%"
    echo Изменения в %filename% отменены
)

if "%choice%"=="8" (
    echo Файлы в staging area:
    git diff --cached --name-only
    echo.
    set /p commit_msg="Введите сообщение коммита: "
    git commit -m "%commit_msg%"
    echo Коммит создан!
)

if "%choice%"=="9" (
    exit /b
)

echo.
echo Текущий статус:
git status --short

pause
goto :EOF
