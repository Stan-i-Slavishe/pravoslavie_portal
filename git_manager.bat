@echo off
title Управление Git - Православный портал
color 0A

:MENU
cls
echo ===============================================
echo       УПРАВЛЕНИЕ GIT - ПРАВОСЛАВНЫЙ ПОРТАЛ
echo ===============================================
echo.
echo Выберите действие:
echo.
echo 1. Проверить статус Git
echo 2. Быстро закоммитить ВСЕ изменения
echo 3. Выборочный коммит файлов
echo 4. Диагностика проблем Git
echo 5. Посмотреть историю коммитов
echo 6. Создать новую ветку
echo 7. Переключиться на другую ветку
echo 8. Запушить изменения
echo 9. Синхронизировать с удаленным репозиторием
echo 0. Выход
echo.
set /p choice="Ваш выбор (0-9): "

if "%choice%"=="1" call check_git_status.bat
if "%choice%"=="2" call commit_all_changes.bat
if "%choice%"=="3" call selective_commit.bat
if "%choice%"=="4" call git_diagnostics.bat

if "%choice%"=="5" (
    echo Последние 20 коммитов:
    git log --oneline -20 --graph
    pause
)

if "%choice%"=="6" (
    set /p branch_name="Введите имя новой ветки: "
    git checkout -b "%branch_name%"
    echo Создана и активирована ветка: %branch_name%
    pause
)

if "%choice%"=="7" (
    echo Доступные ветки:
    git branch -a
    echo.
    set /p branch_name="Введите имя ветки для переключения: "
    git checkout "%branch_name%"
    pause
)

if "%choice%"=="8" (
    echo Пушим текущую ветку...
    git push
    echo Готово!
    pause
)

if "%choice%"=="9" (
    echo Синхронизируем с удаленным репозиторием...
    git fetch
    git pull
    echo Синхронизация завершена!
    pause
)

if "%choice%"=="0" exit /b

goto MENU
