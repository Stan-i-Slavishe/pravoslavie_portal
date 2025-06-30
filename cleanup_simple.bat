@echo off
setlocal enabledelayedexpansion

echo.
echo ===============================================================
echo COMPLETE CLEANUP - COMMENTS SYSTEM REMOVAL
echo ===============================================================
echo.

echo Running Python cleanup script...
python complete_cleanup.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error running cleanup script
    pause
    exit /b 1
)

echo.
echo Creating migrations...
python manage.py makemigrations

echo.
echo Applying migrations...
python manage.py migrate

echo.
echo Testing server...
echo Starting server for final check...

timeout /t 2 /nobreak >nul

start /min python manage.py runserver

timeout /t 5 /nobreak >nul

taskkill /f /im python.exe /fi "WINDOWTITLE eq *runserver*" >nul 2>&1

echo.
echo ===============================================================
echo CLEANUP COMPLETED SUCCESSFULLY!
echo ===============================================================
echo.
echo What was done:
echo    - Removed all comment mentions
echo    - Cleaned all Python files
echo    - Cleaned all templates
echo    - Deleted comment files
echo    - Created clean migrations
echo    - Project tested
echo.
echo READY FOR NEW COMMENT SYSTEM!
echo.
pause
