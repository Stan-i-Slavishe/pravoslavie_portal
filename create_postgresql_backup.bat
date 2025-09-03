@echo off
REM ==========================================
REM СОЗДАНИЕ РЕЗЕРВНОЙ КОПИИ POSTGRESQL
REM ==========================================

echo.
echo ========================================
echo     СОЗДАНИЕ БЭКАПА POSTGRESQL
echo ========================================
echo.

REM Создание папки для бэкапов с датой
set BACKUP_DATE=%date:~-4,4%-%date:~-7,2%-%date:~-10,2%
set BACKUP_TIME=%time:~0,2%-%time:~3,2%-%time:~6,2%
set BACKUP_TIME=%BACKUP_TIME: =0%
set BACKUP_DIR=backups\postgresql_%BACKUP_DATE%_%BACKUP_TIME%

if not exist "backups" mkdir backups
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo 📁 Создана папка бэкапа: %BACKUP_DIR%
echo.

echo 🗄️ Создание дампа базы данных...

REM SQL дамп (читаемый формат)
echo 📄 Создаем SQL дамп...
pg_dump -U pravoslavie_user -h localhost -d pravoslavie_local_db ^
        --no-password ^
        --verbose ^
        --file="%BACKUP_DIR%\database.sql"

if errorlevel 1 (
    echo ❌ Ошибка создания SQL дампа
    echo 💡 Убедитесь что:
    echo    - PostgreSQL запущен
    echo    - pg_dump доступен в PATH
    echo    - Пароль правильный
    pause
    exit /b 1
)

echo ✅ SQL дамп создан: %BACKUP_DIR%\database.sql

REM Сжатый дамп (для хранения)
echo 📦 Создаем сжатый дамп...
pg_dump -U pravoslavie_user -h localhost -d pravoslavie_local_db ^
        --no-password ^
        --format=custom ^
        --compress=9 ^
        --verbose ^
        --file="%BACKUP_DIR%\database.dump"

if errorlevel 1 (
    echo ❌ Ошибка создания сжатого дампа
) else (
    echo ✅ Сжатый дамп создан: %BACKUP_DIR%\database.dump
)

echo.
echo 📁 Копирование медиа-файлов...

REM Копирование папки media
if exist "media" (
    xcopy "media" "%BACKUP_DIR%\media\" /E /I /H /Y >nul
    echo ✅ Медиа-файлы скопированы
) else (
    echo ⚠️ Папка media не найдена
)

echo.
echo 📝 Создание информационного файла...

REM Создание info файла с информацией о бэкапе
(
echo РЕЗЕРВНАЯ КОПИЯ POSTGRESQL - ПРАВОСЛАВНЫЙ ПОРТАЛ
echo ================================================
echo.
echo Дата создания: %date% %time%
echo База данных: pravoslavie_local_db
echo Пользователь: pravoslavie_user
echo Хост: localhost
echo Порт: 5432
echo.
echo СОДЕРЖИМОЕ БЭКАПА:
echo - database.sql     : SQL дамп БД ^(читаемый^)
echo - database.dump    : Сжатый дамп БД ^(для pg_restore^)
echo - media\           : Медиа-файлы ^(изображения, PDF^)
echo.
echo ВОССТАНОВЛЕНИЕ:
echo 1. SQL дамп:  psql -U pravoslavie_user -d pravoslavie_local_db -f database.sql
echo 2. Dump файл: pg_restore -U pravoslavie_user -d pravoslavie_local_db database.dump
echo.
echo РАЗМЕРЫ ФАЙЛОВ:
) > "%BACKUP_DIR%\backup_info.txt"

REM Добавляем размеры файлов в info
for %%F in ("%BACKUP_DIR%\*.*") do (
    echo %%~nxF : %%~zF байт >> "%BACKUP_DIR%\backup_info.txt"
)

echo ✅ Информационный файл создан

echo.
echo 🧪 Проверка целостности бэкапа...

REM Проверка что файлы созданы
if exist "%BACKUP_DIR%\database.sql" (
    echo ✅ SQL дамп найден
) else (
    echo ❌ SQL дамп не создан
)

if exist "%BACKUP_DIR%\database.dump" (
    echo ✅ Сжатый дамп найден
) else (
    echo ❌ Сжатый дамп не создан
)

if exist "%BACKUP_DIR%\media" (
    echo ✅ Медиа-файлы найдены
) else (
    echo ⚠️ Медиа-файлы не найдены
)

echo.
echo ==========================================
echo        ✅ РЕЗЕРВНОЕ КОПИРОВАНИЕ ЗАВЕРШЕНО!
echo ==========================================
echo.
echo 📂 Бэкап сохранен в: %BACKUP_DIR%
echo.
echo 📋 Содержимое бэкапа:
dir /B "%BACKUP_DIR%"
echo.
echo 💾 Рекомендации по хранению бэкапов:
echo    - Храните бэкапы в безопасном месте
echo    - Регулярно создавайте новые бэкапы
echo    - Тестируйте восстановление из бэкапов
echo    - Используйте внешние накопители для хранения
echo.
pause