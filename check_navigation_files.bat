@echo off
echo ================================================================================================
echo                                🔍 ПРОВЕРКА ФАЙЛОВ ИСПРАВЛЕНИЯ
echo ================================================================================================
echo.

set "all_good=true"

echo Проверяем наличие всех необходимых файлов...
echo.

REM Проверка CSS файла
if exist "static\css\mobile-navigation-critical-fix.css" (
    echo ✅ CSS исправление: static\css\mobile-navigation-critical-fix.css
) else (
    echo ❌ ОТСУТСТВУЕТ: static\css\mobile-navigation-critical-fix.css
    set "all_good=false"
)

REM Проверка JS файла  
if exist "static\js\mobile-navigation-fix.js" (
    echo ✅ JavaScript исправление: static\js\mobile-navigation-fix.js
) else (
    echo ❌ ОТСУТСТВУЕТ: static\js\mobile-navigation-fix.js
    set "all_good=false"
)

REM Проверка базового шаблона
if exist "templates\base.html" (
    echo ✅ Базовый шаблон: templates\base.html
) else (
    echo ❌ ОТСУТСТВУЕТ: templates\base.html
    set "all_good=false"
)

REM Проверка скриптов запуска
if exist "apply_navigation_fix_detailed.bat" (
    echo ✅ Детальный скрипт запуска: apply_navigation_fix_detailed.bat
) else (
    echo ❌ ОТСУТСТВУЕТ: apply_navigation_fix_detailed.bat
    set "all_good=false"
)

if exist "test_mobile_navigation.html" (
    echo ✅ Тест-страница: test_mobile_navigation.html
) else (
    echo ❌ ОТСУТСТВУЕТ: test_mobile_navigation.html  
    set "all_good=false"
)

echo.
echo ================================================================================================

if "%all_good%"=="true" (
    echo                                      🎉 ВСЕ ФАЙЛЫ НА МЕСТЕ!
    echo.
    echo Исправления готовы к применению. Запустите:
    echo   apply_navigation_fix_detailed.bat
    echo.
    echo Или протестируйте вручную:
    echo   1. python manage.py collectstatic --noinput
    echo   2. python manage.py runserver
    echo   3. Откройте http://127.0.0.1:8000/shop/?type=subscription
    echo   4. Включите мобильный режим F12 ^> Toggle Device Toolbar
    echo   5. Проверьте, что бургер-меню не пересекается с другими элементами
) else (
    echo                                      ❌ НЕКОТОРЫЕ ФАЙЛЫ ОТСУТСТВУЮТ!
    echo.
    echo Пожалуйста, убедитесь, что все файлы созданы правильно.
)

echo ================================================================================================
pause
