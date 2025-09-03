@echo off
chcp 65001 >nul
REM ==========================================
REM МАСТЕР-СКРИПТ ПЕРЕХОДА НА POSTGRESQL
REM ==========================================

title Перевод на PostgreSQL - Православный портал

:MENU
cls
echo.
echo ================================================
echo    ПЕРЕВОД НА POSTGRESQL - ПРАВОСЛАВНЫЙ ПОРТАЛ
echo ================================================
echo.
echo Выберите действие:
echo.
echo    1. Установить и настроить PostgreSQL
echo    2. Мигрировать данные из SQLite в PostgreSQL  
echo    3. Проверить целостность данных после миграции
echo    4. Создать резервную копию PostgreSQL
echo    5. Запустить сайт на PostgreSQL
echo    6. Показать статус системы
echo.
echo    0. Выход
echo.
set /p choice=Введите номер действия: 

if "%choice%"=="1" goto INSTALL_POSTGRESQL
if "%choice%"=="2" goto MIGRATE_DATA  
if "%choice%"=="3" goto CHECK_DATA
if "%choice%"=="4" goto CREATE_BACKUP
if "%choice%"=="5" goto RUN_SITE
if "%choice%"=="6" goto SHOW_STATUS
if "%choice%"=="0" goto EXIT
goto MENU

:INSTALL_POSTGRESQL
cls
echo.
echo ================================================
echo        УСТАНОВКА И НАСТРОЙКА POSTGRESQL
echo ================================================
echo.
call setup_postgresql.bat
pause
goto MENU

:MIGRATE_DATA
cls  
echo.
echo ================================================
echo          МИГРАЦИЯ ДАННЫХ SQLite -^> PostgreSQL
echo ================================================
echo.
call migrate_to_postgresql.bat
pause
goto MENU

:CHECK_DATA
cls
echo.
echo ================================================
echo        ПРОВЕРКА ЦЕЛОСТНОСТИ ДАННЫХ
echo ================================================
echo.
if not exist ".venv\Scripts\activate.bat" (
    echo Виртуальное окружение не найдено!
    pause
    goto MENU
)
call .venv\Scripts\activate.bat
python check_migration.py
pause
goto MENU

:CREATE_BACKUP
cls
echo.
echo ================================================
echo         СОЗДАНИЕ РЕЗЕРВНОЙ КОПИИ
echo ================================================
echo.
call create_postgresql_backup.bat
pause
goto MENU

:RUN_SITE
cls
echo.
echo ================================================
echo           ЗАПУСК САЙТА НА POSTGRESQL
echo ================================================
echo.
if not exist ".venv\Scripts\activate.bat" (
    echo Виртуальное окружение не найдено!
    pause
    goto MENU
)

call .venv\Scripts\activate.bat

echo Проверяем подключение к PostgreSQL...
python manage.py check --database default
if errorlevel 1 (
    echo Проблемы с подключением к PostgreSQL
    echo Выполните сначала пункты 1 и 2
    pause
    goto MENU
)

echo Подключение к PostgreSQL успешно
echo.
echo Запуск сервера разработки...
echo Для остановки нажмите Ctrl+C
echo.
python manage.py runserver 127.0.0.1:8000
pause
goto MENU

:SHOW_STATUS
cls
echo.
echo ================================================
echo              СТАТУС СИСТЕМЫ
echo ================================================
echo.

REM Проверка PostgreSQL
echo PostgreSQL:
pg_dump --version >nul 2>&1
if errorlevel 1 (
    echo    PostgreSQL не установлен или не в PATH
) else (
    echo    PostgreSQL установлен
    pg_dump --version
)

echo.

REM Проверка виртуального окружения
echo Python окружение:
if exist ".venv\Scripts\activate.bat" (
    echo    Виртуальное окружение найдено
) else (
    echo    Виртуальное окружение не найдено
)

echo.

REM Проверка конфигурации
echo Конфигурация:
if exist ".env.local" (
    echo    Файл .env.local найден
    findstr "USE_SQLITE" .env.local >nul 2>&1
    if errorlevel 1 (
        echo    Настройки БД не определены
    ) else (
        findstr "USE_SQLITE=False" .env.local >nul 2>&1
        if errorlevel 1 (
            echo    Настроен на SQLite
        ) else (
            echo    Настроен на PostgreSQL
        )
    )
) else (
    echo    Файл .env.local не найден
)

echo.

REM Проверка данных  
echo Данные:
if exist "db.sqlite3" (
    echo    SQLite БД найдена ^(размер: 
    for %%A in ("db.sqlite3") do echo %%~zA байт^)
) else (
    echo    SQLite БД не найдена
)

if exist "backups" (
    echo    Папка backups найдена
    for /f %%i in ('dir /b backups\*.json 2^>nul ^| find /c /v ""') do echo        Экспортов SQLite: %%i
    for /f %%i in ('dir /b backups\*.sql 2^>nul ^| find /c /v ""') do echo        Бэкапов PostgreSQL: %%i
) else (
    echo    Папка backups не найдена
)

echo.

REM Статус подключения к PostgreSQL (если окружение есть)
if exist ".venv\Scripts\activate.bat" (
    echo Тест подключения к PostgreSQL:
    call .venv\Scripts\activate.bat >nul 2>&1
    python manage.py check --database default >nul 2>&1
    if errorlevel 1 (
        echo    Не удалось подключиться к PostgreSQL
    ) else (
        echo    PostgreSQL подключена и работает
    )
)

echo.
echo ================================================
pause
goto MENU

:EXIT
cls
echo.
echo ============================================
echo    Спасибо за использование скрипта!
echo ============================================
echo.
echo ИТОГИ РАБОТЫ:
echo    Готовые скрипты для перевода на PostgreSQL
echo    Автоматизированная миграция данных
echo    Проверка целостности после переноса
echo    Система резервного копирования
echo.
echo СЛЕДУЮЩИЕ ЭТАПЫ:
echo    1. Docker контейнеризация
echo    2. Деплой на продакшн сервер
echo    3. Настройка CI/CD pipeline
echo.
echo Все скрипты сохранены в корне проекта
echo.
pause
exit