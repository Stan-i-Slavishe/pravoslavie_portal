@echo off
REM ==========================================
REM CREATE POSTGRESQL BACKUP
REM ==========================================

echo.
echo ========================================
echo     CREATE POSTGRESQL BACKUP
echo ========================================
echo.

REM Create backup folder with date
set BACKUP_DATE=%date:~-4,4%-%date:~-7,2%-%date:~-10,2%
set BACKUP_TIME=%time:~0,2%-%time:~3,2%-%time:~6,2%
set BACKUP_TIME=%BACKUP_TIME: =0%
set BACKUP_DIR=backups\postgresql_%BACKUP_DATE%_%BACKUP_TIME%

if not exist "backups" mkdir backups
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo Created backup folder: %BACKUP_DIR%
echo.

echo Creating database dump...

REM SQL dump (readable format)
echo Creating SQL dump...
pg_dump -U pravoslavie_user -h localhost -d pravoslavie_local_db ^
        --no-password ^
        --verbose ^
        --file="%BACKUP_DIR%\database.sql"

if errorlevel 1 (
    echo Error creating SQL dump
    echo Make sure:
    echo    - PostgreSQL is running
    echo    - pg_dump is available in PATH
    echo    - Password is correct
    pause
    exit /b 1
)

echo SQL dump created: %BACKUP_DIR%\database.sql

REM Compressed dump (for storage)
echo Creating compressed dump...
pg_dump -U pravoslavie_user -h localhost -d pravoslavie_local_db ^
        --no-password ^
        --format=custom ^
        --compress=9 ^
        --verbose ^
        --file="%BACKUP_DIR%\database.dump"

if errorlevel 1 (
    echo Error creating compressed dump
) else (
    echo Compressed dump created: %BACKUP_DIR%\database.dump
)

echo.
echo Copying media files...

REM Copy media folder
if exist "media" (
    xcopy "media" "%BACKUP_DIR%\media\" /E /I /H /Y >nul
    echo Media files copied
) else (
    echo Media folder not found
)

echo.
echo Creating info file...

REM Create info file with backup information
(
echo POSTGRESQL BACKUP - PRAVOSLAVIE PORTAL
echo ================================================
echo.
echo Created: %date% %time%
echo Database: pravoslavie_local_db
echo User: pravoslavie_user
echo Host: localhost
echo Port: 5432
echo.
echo BACKUP CONTENTS:
echo - database.sql     : SQL dump ^(readable^)
echo - database.dump    : Compressed dump ^(for pg_restore^)
echo - media\           : Media files ^(images, PDFs^)
echo.
echo RESTORE:
echo 1. SQL dump:  psql -U pravoslavie_user -d pravoslavie_local_db -f database.sql
echo 2. Dump file: pg_restore -U pravoslavie_user -d pravoslavie_local_db database.dump
echo.
echo FILE SIZES:
) > "%BACKUP_DIR%\backup_info.txt"

REM Add file sizes to info
for %%F in ("%BACKUP_DIR%\*.*") do (
    echo %%~nxF : %%~zF bytes >> "%BACKUP_DIR%\backup_info.txt"
)

echo Info file created

echo.
echo Checking backup integrity...

REM Check that files were created
if exist "%BACKUP_DIR%\database.sql" (
    echo SQL dump found
) else (
    echo SQL dump not created
)

if exist "%BACKUP_DIR%\database.dump" (
    echo Compressed dump found
) else (
    echo Compressed dump not created
)

if exist "%BACKUP_DIR%\media" (
    echo Media files found
) else (
    echo Media files not found
)

echo.
echo ==========================================
echo        BACKUP COMPLETED!
echo ==========================================
echo.
echo Backup saved to: %BACKUP_DIR%
echo.
echo Backup contents:
dir /B "%BACKUP_DIR%"
echo.
echo Backup storage recommendations:
echo    - Store backups in a safe place
echo    - Create regular backups
echo    - Test backup restoration
echo    - Use external drives for storage
echo.
pause