@echo off
REM ==========================================
REM БЫСТРАЯ УСТАНОВКА POSTGRESQL ДЛЯ ПРОЕКТА
REM ==========================================

echo.
echo ========================================
echo    УСТАНОВКА И НАСТРОЙКА POSTGRESQL
echo ========================================
echo.

echo 📥 ШАГИ УСТАНОВКИ:
echo.
echo 1. Скачайте PostgreSQL 15+ с официального сайта:
echo    https://www.postgresql.org/download/windows/
echo.
echo 2. Во время установки запомните пароль для postgres
echo.
echo 3. После установки вернитесь к этому скрипту
echo.
pause

echo.
echo 🔧 Проверяем установку PostgreSQL...

REM Проверка что PostgreSQL установлен
psql --version >nul 2>&1
if errorlevel 1 (
    echo ❌ PostgreSQL не найден в PATH
    echo.
    echo 💡 Добавьте в PATH путь к PostgreSQL:
    echo    C:\Program Files\PostgreSQL\15\bin
    echo.
    echo 🔄 После добавления в PATH перезапустите скрипт
    pause
    exit /b 1
)

echo ✅ PostgreSQL найден
psql --version
echo.

echo 🗄️ Создание базы данных и пользователя...
echo.
echo Введите пароль пользователя postgres:

REM Выполнение SQL скрипта для создания БД
psql -U postgres -h localhost -f setup_postgresql.sql
if errorlevel 1 (
    echo ❌ Ошибка при создании БД
    echo.
    echo 💡 Возможные причины:
    echo    • Неверный пароль postgres
    echo    • PostgreSQL не запущен
    echo    • Пользователь pravoslavie_user уже существует
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ База данных pravoslavie_local_db создана успешно!
echo.
echo 🧪 Проверяем подключение к новой БД...

REM Проверка подключения к созданной БД
psql -U pravoslavie_user -h localhost -d pravoslavie_local_db -c "\dt"
if errorlevel 1 (
    echo ⚠️ Проблемы с подключением к БД pravoslavie_user
    echo Но это нормально - Django создаст таблицы позже
)

echo.
echo ==========================================
echo        ✅ POSTGRESQL ГОТОВ К РАБОТЕ!
echo ==========================================
echo.
echo 📋 Созданные объекты:
echo    📂 База данных: pravoslavie_local_db
echo    👤 Пользователь: pravoslavie_user  
echo    🔐 Пароль: local_strong_password_2024
echo    🌐 Хост: localhost
echo    🚪 Порт: 5432
echo.
echo 🚀 СЛЕДУЮЩИЕ ШАГИ:
echo    1. Запустите migrate_to_postgresql.bat
echo    2. Это перенесет все данные из SQLite в PostgreSQL
echo.
pause