@echo off
REM ==========================================
REM CREATE POSTGRESQL BACKUP - IMPROVED
REM ==========================================

echo.
echo ========================================
echo     CREATE POSTGRESQL BACKUP
echo ========================================
echo.

REM Set environment variables for PostgreSQL authentication
set PGPASSWORD=local_strong_password_2024
set PGUSER=pravoslavie_user
set PGHOST=localhost
set PGPORT=5432
set PGDATABASE=pravoslavie_local_db

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
echo Database: %PGDATABASE%
echo User: %PGUSER%
echo.

REM SQL dump (readable format)
echo Creating SQL dump...
pg_dump --verbose --file="%BACKUP_DIR%\database.sql" --format=plain --no-owner --no-privileges
if errorlevel 1 (
    echo Error creating SQL dump
    echo.
    echo Trying alternative method...
    pg_dump -h %PGHOST% -p %PGPORT% -U %PGUSER% -d %PGDATABASE% -f "%BACKUP_DIR%\database.sql" --no-password --verbose
    if errorlevel 1 (
        echo Could not create backup
        echo Check that PostgreSQL is running and credentials are correct
        pause
        exit /b 1
    )
)

echo SQL dump created: %BACKUP_DIR%\database.sql

REM Compressed dump (for storage)
echo Creating compressed dump...
pg_dump --verbose --file="%BACKUP_DIR%\database.dump" --format=custom --compress=9 --no-owner --no-privileges
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
echo Database: %PGDATABASE%
echo User: %PGUSER%
echo Host: %PGHOST%
echo Port: %PGPORT%
echo.
echo BACKUP CONTENTS:
echo - database.sql     : SQL dump ^(readable^)
echo - database.dump    : Compressed dump ^(for pg_restore^)
echo - media\           : Media files ^(images, PDFs^)
echo.
echo RESTORE COMMANDS:
echo 1. SQL dump:
echo    psql -h %PGHOST% -p %PGPORT% -U %PGUSER% -d %PGDATABASE% -f database.sql
echo.
echo 2. Compressed dump:
echo    pg_restore -h %PGHOST% -p %PGPORT% -U %PGUSER% -d %PGDATABASE% database.dump
echo.
echo 3. Create new database and restore:
echo    createdb -h %PGHOST% -p %PGPORT% -U %PGUSER% pravoslavie_restored_db
echo    pg_restore -h %PGHOST% -p %PGPORT% -U %PGUSER% -d pravoslavie_restored_db database.dump
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
    for %%A in ("%BACKUP_DIR%\database.sql") do echo    Size: %%~zA bytes
) else (
    echo SQL dump not created
)

if exist "%BACKUP_DIR%\database.dump" (
    echo Compressed dump found
    for %%A in ("%BACKUP_DIR%\database.dump") do echo    Size: %%~zA bytes
) else (
    echo Compressed dump not created
)

if exist "%BACKUP_DIR%\media" (
    echo Media files found
    for /f %%i in ('dir /s /b "%BACKUP_DIR%\media" ^| find /c /v ""') do echo    Files: %%i
) else (
    echo Media files not found
)

echo.
echo Creating Django fixture backup...

REM Also create Django fixture as additional backup
echo Creating Django data export...
set DJANGO_ENV=local
python manage.py dumpdata --natural-foreign --natural-primary --settings=config.settings_local -o "%BACKUP_DIR%\django_data.json"
if errorlevel 1 (
    echo Could not create Django fixture
) else (
    echo Django fixture created: %BACKUP_DIR%\django_data.json
)

echo.
echo ==========================================
echo        BACKUP COMPLETED SUCCESSFULLY!
echo ==========================================
echo.
echo Backup location: %BACKUP_DIR%
echo.
echo Contents:
dir /B "%BACKUP_DIR%"
echo.
echo Total backup size:
for /f %%A in ('dir "%BACKUP_DIR%" /s /-c /q ^| find "File(s)"') do echo %%A

echo.
echo Backup recommendations:
echo   - Store in secure location
echo   - Test restore procedure
echo   - Keep multiple backup versions
echo   - Use external storage for safety
echo.

REM Clear password from environment
set PGPASSWORD=

pause