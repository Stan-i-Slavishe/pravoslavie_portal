@echo off
echo Collecting static files...
python manage.py collectstatic --noinput
echo.
echo Static files collected!
echo.
echo MOBILE NAVIGATION FIX APPLIED SUCCESSFULLY!
echo.
echo Changes:
echo   - Created mobile-cart-left.css
echo   - Added cart button to left top corner
echo   - Updated JavaScript to handle both cart buttons
echo   - CSS linked in base.html
echo.
echo Next: Restart Django server and test on mobile!
echo   python manage.py runserver
echo.
pause