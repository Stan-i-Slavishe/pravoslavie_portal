@echo off
echo ===============================================
echo RESTORING FAIRY TALES SYSTEM
echo ===============================================
echo.

echo Step 1: Copying new views...
copy /Y restored_views.py fairy_tales\views.py
if %errorlevel% == 0 (
    echo Views updated successfully
) else (
    echo Error copying views
    pause
    exit /b 1
)

echo.
echo Step 2: Copying new URLs...
copy /Y restored_urls.py fairy_tales\urls.py
if %errorlevel% == 0 (
    echo URLs updated successfully
) else (
    echo Error copying URLs
    pause
    exit /b 1
)

echo.
echo Step 3: Applying migrations...
python manage.py makemigrations fairy_tales
python manage.py migrate
if %errorlevel% == 0 (
    echo Migrations applied successfully
) else (
    echo Error applying migrations
    pause
    exit /b 1
)

echo.
echo Step 4: Creating test data...
python create_fairy_tales_data.py
if %errorlevel% == 0 (
    echo Test data created successfully
) else (
    echo Error creating test data
    pause
    exit /b 1
)

echo.
echo Step 5: Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% == 0 (
    echo Static files collected successfully
) else (
    echo Error collecting static files
    echo Continuing without critical error...
)

echo.
echo ===============================================
echo FAIRY TALES SYSTEM SUCCESSFULLY RESTORED!
echo ===============================================
echo.
echo Available features:
echo   - Tales catalog: /fairy-tales/
echo   - Categories: /fairy-tales/categories/
echo   - Tale personalization
echo   - Favorite system
echo   - Reviews and ratings
echo   - Personalization orders
echo.
echo Created categories:
echo   - Overcoming fears
echo   - Building confidence
echo   - Improving relationships
echo   - Behavior correction
echo   - Emotion management
echo   - Spiritual education
echo.
echo Start server: python manage.py runserver
echo Open browser: http://127.0.0.1:8000/fairy-tales/
echo.
pause
