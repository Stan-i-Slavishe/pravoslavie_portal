@echo off
chcp 65001 >nul
title Деплой на продакшн

echo.
echo ╔════════════════════════════════════════╗
echo ║   🚀 ДЕПЛОЙ НА ПРОДАКШН СЕРВЕР        ║
echo ╚════════════════════════════════════════╝
echo.

:menu
echo Выберите действие:
echo.
echo [1] 📋 Проверить готовность к деплою
echo [2] 📦 Коммит и Push изменений
echo [3] 🚀 Только Push (коммит уже сделан)
echo [4] 📝 Показать команды для сервера
echo [5] 🌐 Открыть админ-панель продакшена
echo [6] 📚 Показать документацию
echo [7] ❌ Выход
echo.
set /p choice="Ваш выбор (1-7): "

if "%choice%"=="1" goto check_ready
if "%choice%"=="2" goto commit_push
if "%choice%"=="3" goto just_push
if "%choice%"=="4" goto show_server_commands
if "%choice%"=="5" goto open_admin
if "%choice%"=="6" goto show_docs
if "%choice%"=="7" goto end

echo.
echo ❌ Неверный выбор!
echo.
goto menu

:check_ready
echo.
echo 🔍 Проверка файлов...
echo.

REM Проверяем основные файлы
echo 📁 Основные файлы:
if exist "core\middleware\maintenance.py" (echo ✅ core\middleware\maintenance.py) else (echo ❌ core\middleware\maintenance.py)
if exist "core\context_processors.py" (echo ✅ core\context_processors.py) else (echo ❌ core\context_processors.py)
if exist "config\settings_base.py" (echo ✅ config\settings_base.py) else (echo ❌ config\settings_base.py)
if exist "templates\includes\maintenance_indicator.html" (echo ✅ templates\includes\maintenance_indicator.html) else (echo ❌ templates\includes\maintenance_indicator.html)
if exist "templates\maintenance.html" (echo ✅ templates\maintenance.html) else (echo ❌ templates\maintenance.html)

echo.
echo 📊 Git статус:
git status --short
echo.
pause
cls
goto menu

:commit_push
echo.
echo 📦 Коммит и Push изменений...
echo.
set /p commit_msg="Введите сообщение коммита (или Enter для стандартного): "

if "%commit_msg%"=="" (
    set commit_msg=feat: режим обслуживания с доступом для администраторов
)

echo.
echo Выполняю команды:
echo   git add .
echo   git commit -m "%commit_msg%"
echo   git push origin main
echo.

git add .
git commit -m "%commit_msg%"
git push origin main

echo.
if %errorlevel% equ 0 (
    echo ✅ Изменения успешно отправлены на GitHub!
    echo.
    echo 📝 Теперь выполните на сервере:
    echo    ssh root@46.62.167.17
    echo    cd /var/www/pravoslavie_portal
    echo    source venv/bin/activate
    echo    ./deploy.sh
) else (
    echo ❌ Ошибка при отправке изменений
)
echo.
pause
cls
goto menu

:just_push
echo.
echo 📤 Отправка изменений...
echo.
git push origin main
echo.
if %errorlevel% equ 0 (
    echo ✅ Изменения успешно отправлены!
) else (
    echo ❌ Ошибка при отправке
)
echo.
pause
cls
goto menu

:show_server_commands
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    📝 КОМАНДЫ ДЛЯ ВЫПОЛНЕНИЯ НА СЕРВЕРЕ
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 1. Подключение к серверу:
echo    ssh root@46.62.167.17
echo    Пароль: vRgFjmEpCVvjXeLTJn7
echo.
echo 2. Переход в проект и активация venv:
echo    cd /var/www/pravoslavie_portal
echo    source venv/bin/activate
echo.
echo 3. Деплой:
echo    ./deploy.sh
echo.
echo 4. Проверка режима обслуживания:
echo    python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); print(f'Режим: {\"🔴 ВКЛ\" if s.maintenance_mode else \"🟢 ВЫКЛ\"}')"
echo.
echo 5. Включить режим (через SSH):
echo    python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = True; s.save(); print('✅ Включен')"
echo.
echo 6. Выключить режим (через SSH):
echo    python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('✅ Выключен')"
echo.
echo 7. Просмотр логов:
echo    sudo journalctl -u gunicorn -f
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
cls
goto menu

:open_admin
echo.
echo 🌐 Открываю админ-панель продакшена...
start https://dobrist.com/admin/core/sitesettings/1/change/
echo.
echo ✅ Страница открыта в браузере
echo.
pause
cls
goto menu

:show_docs
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo           📚 ДОКУМЕНТАЦИЯ
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📄 Доступные документы:
echo.
echo 1. PRODUCTION_DEPLOY.md
echo    └─ Подробная инструкция по деплою
echo.
echo 2. MAINTENANCE_MODE_GUIDE.md
echo    └─ Полное руководство по режиму обслуживания
echo.
echo 3. MIDDLEWARE_ORDER_FIX.md
echo    └─ Объяснение исправления порядка middleware
echo.
echo 4. MAINTENANCE_CHECKLIST.md
echo    └─ Чек-лист проверки системы
echo.
echo 5. MAINTENANCE_READY_FINAL.md
echo    └─ Итоговый документ с решением
echo.
echo 🛠️ Инструменты:
echo.
echo - test_maintenance_mode.py
echo   └─ Скрипт проверки и управления
echo.
echo - maintenance_control.bat
echo   └─ Меню управления (локально)
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
cls
goto menu

:end
echo.
echo 👋 До свидания!
timeout /t 2 >nul
exit
