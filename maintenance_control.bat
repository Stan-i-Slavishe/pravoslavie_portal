@echo off
chcp 65001 >nul
title Управление режимом обслуживания

echo.
echo ================================
echo   РЕЖИМ ОБСЛУЖИВАНИЯ
echo ================================
echo.

:menu
echo Выберите действие:
echo.
echo [1] Проверить статус
echo [2] ВКЛЮЧИТЬ режим обслуживания
echo [3] ВЫКЛЮЧИТЬ режим обслуживания
echo [4] Открыть настройки в админке
echo [5] Выход
echo.
set /p choice="Ваш выбор (1-5): "

if "%choice%"=="1" goto check_status
if "%choice%"=="2" goto enable_maintenance
if "%choice%"=="3" goto disable_maintenance
if "%choice%"=="4" goto open_admin
if "%choice%"=="5" goto end

echo.
echo ❌ Неверный выбор! Попробуйте снова.
echo.
goto menu

:check_status
echo.
echo 🔍 Проверка статуса...
echo.
python test_maintenance_mode.py
echo.
pause
cls
goto menu

:enable_maintenance
echo.
echo 🔴 Включение режима обслуживания...
echo.
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = True; s.maintenance_message = 'Мы проводим плановые работы. Сайт будет доступен в ближайшее время.'; s.save(); print('✅ Режим обслуживания ВКЛЮЧЕН')"
echo.
echo ✅ Готово! Администраторы по-прежнему имеют доступ.
echo.
pause
cls
goto menu

:disable_maintenance
echo.
echo 🟢 Выключение режима обслуживания...
echo.
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('✅ Режим обслуживания ВЫКЛЮЧЕН')"
echo.
echo ✅ Готово! Сайт доступен всем пользователям.
echo.
pause
cls
goto menu

:open_admin
echo.
echo 🌐 Открытие админ-панели...
start http://localhost:8000/admin/core/sitesettings/1/change/
echo.
echo ✅ Страница настроек открыта в браузере
echo.
pause
cls
goto menu

:end
echo.
echo 👋 До свидания!
timeout /t 2 >nul
exit
