@echo off
echo ========================================
echo   IMPROVING CLOSE BUTTON
echo ========================================
echo.

echo Changes made:
echo - Round shape with shadow
echo - Hover effects with scale and rotation
echo - Smooth animations
echo - Better mobile experience
echo.

echo Apply improvements? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo.
    echo Collecting static files...
    python manage.py collectstatic --noinput 2>nul
    echo Done!
    
    echo.
    echo Restarting Django server...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2
    start cmd /k "cd /d %~dp0 && python manage.py runserver"
    echo Server restarted!
    
    echo.
    echo Open browser? (y/n)
    set /p open_choice=
    if /i "%open_choice%"=="y" (
        timeout /t 3
        start http://127.0.0.1:8000/stories/
    )
)

echo.
echo DONE! Close button is now much better!
echo.
echo To test:
echo 1. Open site on mobile
echo 2. Click "Add comment"
echo 3. Look at the X button
echo 4. Hover - button scales up and rotates
echo 5. Click - smooth close animation
echo.

pause
