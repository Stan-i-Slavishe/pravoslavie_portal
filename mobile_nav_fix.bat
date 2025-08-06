@echo off
chcp 65001 > nul
title Mobile Navigation Fix - Cart Left, Burger Right

echo =====================================
echo MOBILE NAVIGATION FIX
echo =====================================
echo.
echo Problem: Cart and burger icons overlap
echo Solution: Cart left, burger right
echo.

:: Check if we are in Django project root
if not exist "manage.py" (
    echo ERROR: Run batch file from Django project root!
    echo File manage.py not found in current directory.
    pause
    exit /b 1
)

echo Found manage.py - continuing...
echo.

:: Create backup of base.html
echo Creating backup of base.html...
if exist "templates\base.html" (
    copy "templates\base.html" "templates\base.html.backup_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%" > nul
    echo Backup created successfully
) else (
    echo File templates\base.html not found!
    pause
    exit /b 1
)

:: Create CSS fix file
echo.
echo Creating mobile-navigation-fix.css file...

:: Create folder if it doesn't exist
if not exist "static\css" (
    mkdir "static\css"
    echo Created static\css folder
)

:: Create CSS file with proper escaping
echo /* MOBILE NAVIGATION FIX - Separate cart and burger */ > "static\css\mobile-navigation-fix.css"
echo. >> "static\css\mobile-navigation-fix.css"
echo /* Cart button on the left */ >> "static\css\mobile-navigation-fix.css"
echo .mobile-cart-button { >> "static\css\mobile-navigation-fix.css"
echo     position: fixed; >> "static\css\mobile-navigation-fix.css"
echo     top: 15px; >> "static\css\mobile-navigation-fix.css"
echo     left: 15px; >> "static\css\mobile-navigation-fix.css"
echo     z-index: 1001; >> "static\css\mobile-navigation-fix.css"
echo     display: none; >> "static\css\mobile-navigation-fix.css"
echo     background: rgba(255, 255, 255, 0.9^); >> "static\css\mobile-navigation-fix.css"
echo     backdrop-filter: blur(10px^); >> "static\css\mobile-navigation-fix.css"
echo     border: 1px solid rgba(226, 232, 240, 0.5^); >> "static\css\mobile-navigation-fix.css"
echo     border-radius: 12px; >> "static\css\mobile-navigation-fix.css"
echo     box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1^); >> "static\css\mobile-navigation-fix.css"
echo     width: 48px; >> "static\css\mobile-navigation-fix.css"
echo     height: 48px; >> "static\css\mobile-navigation-fix.css"
echo     align-items: center; >> "static\css\mobile-navigation-fix.css"
echo     justify-content: center; >> "static\css\mobile-navigation-fix.css"
echo     cursor: pointer; >> "static\css\mobile-navigation-fix.css"
echo     transition: all 0.3s ease; >> "static\css\mobile-navigation-fix.css"
echo     text-decoration: none; >> "static\css\mobile-navigation-fix.css"
echo     color: #d69e2e; >> "static\css\mobile-navigation-fix.css"
echo } >> "static\css\mobile-navigation-fix.css"
echo. >> "static\css\mobile-navigation-fix.css"
echo .mobile-cart-button:hover { >> "static\css\mobile-navigation-fix.css"
echo     background: white; >> "static\css\mobile-navigation-fix.css"
echo     transform: scale(1.05^); >> "static\css\mobile-navigation-fix.css"
echo     color: #d69e2e; >> "static\css\mobile-navigation-fix.css"
echo     text-decoration: none; >> "static\css\mobile-navigation-fix.css"
echo } >> "static\css\mobile-navigation-fix.css"
echo. >> "static\css\mobile-navigation-fix.css"
echo .mobile-cart-icon { >> "static\css\mobile-navigation-fix.css"
echo     font-size: 20px; >> "static\css\mobile-navigation-fix.css"
echo } >> "static\css\mobile-navigation-fix.css"
echo. >> "static\css\mobile-navigation-fix.css"
echo .mobile-cart-badge { >> "static\css\mobile-navigation-fix.css"
echo     position: absolute; >> "static\css\mobile-navigation-fix.css"
echo     top: 2px; >> "static\css\mobile-navigation-fix.css"
echo     right: 2px; >> "static\css\mobile-navigation-fix.css"
echo     background: #e53e3e; >> "static\css\mobile-navigation-fix.css"
echo     color: white; >> "static\css\mobile-navigation-fix.css"
echo     font-size: 10px; >> "static\css\mobile-navigation-fix.css"
echo     font-weight: 600; >> "static\css\mobile-navigation-fix.css"
echo     padding: 2px 6px; >> "static\css\mobile-navigation-fix.css"
echo     border-radius: 10px; >> "static\css\mobile-navigation-fix.css"
echo     min-width: 16px; >> "static\css\mobile-navigation-fix.css"
echo     text-align: center; >> "static\css\mobile-navigation-fix.css"
echo } >> "static\css\mobile-navigation-fix.css"
echo. >> "static\css\mobile-navigation-fix.css"
echo /* Hide shop from bottom navigation */ >> "static\css\mobile-navigation-fix.css"
echo .mobile-nav-item[data-section="shop"] { >> "static\css\mobile-navigation-fix.css"
echo     display: none !important; >> "static\css\mobile-navigation-fix.css"
echo } >> "static\css\mobile-navigation-fix.css"
echo. >> "static\css\mobile-navigation-fix.css"
echo .mobile-nav-items { >> "static\css\mobile-navigation-fix.css"
echo     justify-content: space-around !important; >> "static\css\mobile-navigation-fix.css"
echo } >> "static\css\mobile-navigation-fix.css"
echo. >> "static\css\mobile-navigation-fix.css"
echo @media (min-width: 992px^) { >> "static\css\mobile-navigation-fix.css"
echo     .mobile-cart-button { >> "static\css\mobile-navigation-fix.css"
echo         display: none !important; >> "static\css\mobile-navigation-fix.css"
echo     } >> "static\css\mobile-navigation-fix.css"
echo } >> "static\css\mobile-navigation-fix.css"
echo. >> "static\css\mobile-navigation-fix.css"
echo @media (max-width: 991.98px^) { >> "static\css\mobile-navigation-fix.css"
echo     .mobile-cart-button { >> "static\css\mobile-navigation-fix.css"
echo         display: flex !important; >> "static\css\mobile-navigation-fix.css"
echo     } >> "static\css\mobile-navigation-fix.css"
echo     body.has-mobile-nav main.container { >> "static\css\mobile-navigation-fix.css"
echo         padding-top: 80px !important; >> "static\css\mobile-navigation-fix.css"
echo     } >> "static\css\mobile-navigation-fix.css"
echo } >> "static\css\mobile-navigation-fix.css"
echo. >> "static\css\mobile-navigation-fix.css"
echo @media (max-width: 575.98px^) { >> "static\css\mobile-navigation-fix.css"
echo     .mobile-cart-button { >> "static\css\mobile-navigation-fix.css"
echo         top: 12px; >> "static\css\mobile-navigation-fix.css"
echo         left: 12px; >> "static\css\mobile-navigation-fix.css"
echo         width: 44px; >> "static\css\mobile-navigation-fix.css"
echo         height: 44px; >> "static\css\mobile-navigation-fix.css"
echo     } >> "static\css\mobile-navigation-fix.css"
echo     .mobile-cart-icon { >> "static\css\mobile-navigation-fix.css"
echo         font-size: 18px; >> "static\css\mobile-navigation-fix.css"
echo     } >> "static\css\mobile-navigation-fix.css"
echo     body.has-mobile-nav main.container { >> "static\css\mobile-navigation-fix.css"
echo         padding-top: 70px !important; >> "static\css\mobile-navigation-fix.css"
echo     } >> "static\css\mobile-navigation-fix.css"
echo } >> "static\css\mobile-navigation-fix.css"

echo CSS file created successfully!

echo.
echo Updating base.html...
echo Adding CSS link...

:: Add CSS link to base.html using simple method
powershell -Command "(Get-Content 'templates\base.html') -replace '(<link rel=\"stylesheet\" href=\"{%% static ''css/mobile-burger-menu.css'' %%}\">)', '$1%NEWLINE%    <link rel=\"stylesheet\" href=\"{%% static ''css/mobile-navigation-fix.css'' %%}\">' | Set-Content 'templates\base.html'"

echo.
echo Adding cart button HTML...

:: Add cart button before burger menu
powershell -Command "(Get-Content 'templates\base.html' -Raw) -replace '(<!-- Кнопка-бургер в правом верхнем углу -->)', '<!-- Кнопка корзины слева (только на мобильных) -->%NEWLINE%{%% if user.is_authenticated %%}%NEWLINE%<a href=\"{%% url ''shop:cart'' %%}\" class=\"mobile-cart-button\" id=\"mobileCart\" title=\"Корзина\">%NEWLINE%    <i class=\"bi bi-cart3 mobile-cart-icon\"></i>%NEWLINE%    <span class=\"mobile-cart-badge\" id=\"mobile-cart-badge-left\" style=\"display: none;\">0</span>%NEWLINE%</a>%NEWLINE%{%% endif %%}%NEWLINE%%NEWLINE%$1' | Set-Content 'templates\base.html' -NoNewline"

echo.
echo Updating JavaScript...

:: Update JavaScript to handle left cart button
powershell -Command "(Get-Content 'templates\base.html' -Raw) -replace '(console\.log\(''Cart badge updated:'', data\.count\);)', '// Update left cart button badge%NEWLINE%        const leftCartBadge = document.getElementById(''mobile-cart-badge-left'');%NEWLINE%        if (leftCartBadge) {%NEWLINE%            leftCartBadge.textContent = data.count;%NEWLINE%            leftCartBadge.style.display = data.count > 0 ? ''inline'' : ''none'';%NEWLINE%        }%NEWLINE%%NEWLINE%        $1' | Set-Content 'templates\base.html' -NoNewline"

echo.
echo Collecting static files...
python manage.py collectstatic --noinput > nul 2>&1
if %errorlevel% == 0 (
    echo Static files collected successfully!
) else (
    echo Warning: Could not collect static files automatically
    echo Please run: python manage.py collectstatic
)

echo.
echo =====================================
echo MOBILE NAVIGATION FIX COMPLETED!
echo =====================================
echo.
echo Changes made:
echo   Mobile devices:
echo      - Cart button in LEFT top corner
echo      - Burger menu in RIGHT top corner
echo      - Bottom navigation now has 5 sections
echo.
echo   Desktop:
echo      - No changes
echo.
echo Created files:
echo   - static\css\mobile-navigation-fix.css
echo   - Backup: templates\base.html.backup_*
echo.
echo Next steps:
echo   1. Restart Django server: python manage.py runserver
echo   2. Test on mobile device or browser dev tools
echo.
echo All done!

pause