@echo off
echo ========================================
echo   REDUCING COMMENT SPACING
echo ========================================
echo.

echo Changes made:
echo - Comment margin: mb-4 to mb-2 (less space between comments)
echo - Header margin: mb-2 to mb-1 (tighter header spacing)  
echo - Text margin: mb-3 to mb-2 (less space after text)
echo - Comment padding: 1rem to 0.75rem (smaller internal padding)
echo - Actions padding/margin: 0.75rem to 0.5rem (compact actions)
echo.

echo This will make comments more compact and reduce scrolling.
echo.

echo Apply changes? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo.
    echo Collecting static files...
    python manage.py collectstatic --noinput 2>nul
    echo.
    echo Restarting Django server...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2
    start cmd /k "python manage.py runserver"
    echo.
    echo Opening browser...
    timeout /t 3
    start http://127.0.0.1:8000/stories/
    echo.
    echo Done! Comments should now be more compact.
)

pause
