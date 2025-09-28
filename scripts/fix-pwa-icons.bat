@echo off
REM ========================================
REM PWA Icons Fix - Automated Deployment
REM ========================================

echo.
echo ======================================
echo   PWA PUSH NOTIFICATIONS ICON FIX
echo ======================================
echo.

REM Шаг 1: Генерация иконок
echo [1/5] Generating PWA icons...
python scripts\generate_pwa_icons.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to generate icons!
    pause
    exit /b 1
)
echo ✅ Icons generated successfully!
echo.

REM Шаг 2: Проверка созданных файлов
echo [2/5] Verifying icon files...
if not exist "static\icons\icon-96x96.png" (
    echo ❌ Missing: icon-96x96.png
    pause
    exit /b 1
)
if not exist "static\icons\icon-128x128.png" (
    echo ❌ Missing: icon-128x128.png
    pause
    exit /b 1
)
if not exist "static\icons\icon-144x144.png" (
    echo ❌ Missing: icon-144x144.png
    pause
    exit /b 1
)
if not exist "static\icons\icon-384x384.png" (
    echo ❌ Missing: icon-384x384.png
    pause
    exit /b 1
)
if not exist "static\icons\badge-72x72.png" (
    echo ❌ Missing: badge-72x72.png
    pause
    exit /b 1
)
echo ✅ All icon files verified!
echo.

REM Шаг 3: Сборка статики
echo [3/5] Collecting static files...
python manage.py collectstatic --noinput
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to collect static files!
    pause
    exit /b 1
)
echo ✅ Static files collected!
echo.

REM Шаг 4: Git add
echo [4/5] Adding files to Git...
git add static/icons/icon-96x96.png
git add static/icons/icon-128x128.png
git add static/icons/icon-144x144.png
git add static/icons/icon-384x384.png
git add static/icons/badge-72x72.png
git add static/sw.js
git add static/manifest.json
git add scripts/generate_pwa_icons.py
git add docs/PWA_ICONS_GUIDE.md
git add docs/DEPLOY_PWA_ICONS.md
git add PWA_FIX_README.md
echo ✅ Files added to Git!
echo.

REM Шаг 5: Git commit
echo [5/5] Creating Git commit...
git commit -m "🔔 Fix PWA push notification icons" -m "- Added all necessary icon sizes (96, 128, 144, 384)" -m "- Created badge icon for notifications (72x72)" -m "- Updated Service Worker with explicit icon paths" -m "- Updated manifest.json with complete icon set" -m "- Added automatic icon generation script" -m "- Added PWA icons documentation" -m "" -m "Push notifications will now show site icon instead of bell"

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create commit!
    pause
    exit /b 1
)
echo ✅ Commit created successfully!
echo.

echo ======================================
echo   ✨ PWA Icons Fix Complete! ✨
echo ======================================
echo.
echo Next steps:
echo 1. Review changes: git log -1
echo 2. Push to remote: git push origin main
echo 3. Deploy to server (see docs/DEPLOY_PWA_ICONS.md)
echo.
echo Press any key to push to remote (or Ctrl+C to cancel)...
pause > nul

REM Шаг 6: Git push (опционально)
echo.
echo Pushing to remote repository...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo ✅ Successfully pushed to remote!
    echo.
    echo 🚀 Now deploy to server:
    echo    ssh user@server
    echo    cd /path/to/pravoslavie_portal
    echo    git pull origin main
    echo    python manage.py collectstatic --noinput
    echo    sudo systemctl restart gunicorn nginx
) else (
    echo ❌ Failed to push to remote!
    echo Please push manually: git push origin main
)

echo.
pause
