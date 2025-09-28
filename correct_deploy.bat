@echo off
chcp 65001 >nul
title Правильный деплой режима обслуживания

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║  🎯 ПРАВИЛЬНЫЙ ДЕПЛОЙ РЕЖИМА ОБСЛУЖИВАНИЯ           ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 📋 Пошаговая инструкция для безопасного деплоя
echo.
pause

:menu
cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║              МЕНЮ ДЕПЛОЯ                            ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo [1] 📦 ШАГ 1: Коммит и Push (локально)
echo [2] 🚀 ШАГ 2: Показать команды для сервера
echo [3] ✅ ШАГ 3: Инструкция по тестированию
echo [4] 🔍 Диагностика (скопировать команды)
echo [5] 📚 Показать документацию
echo [6] ❌ Выход
echo.
set /p choice="Выберите шаг (1-6): "

if "%choice%"=="1" goto step1
if "%choice%"=="2" goto step2
if "%choice%"=="3" goto step3
if "%choice%"=="4" goto diagnostics
if "%choice%"=="5" goto docs
if "%choice%"=="6" goto end

echo.
echo ❌ Неверный выбор!
timeout /t 2 >nul
goto menu

:step1
cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║         ШАГ 1: КОММИТ И PUSH (ЛОКАЛЬНО)             ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 📝 Сейчас будет выполнен коммит и push на GitHub
echo.
set /p commit_msg="Введите сообщение коммита (Enter = стандартное): "

if "%commit_msg%"=="" (
    set commit_msg=feat: режим обслуживания с доступом для администраторов
)

echo.
echo Выполняю:
echo   1. git add .
echo   2. git commit -m "%commit_msg%"
echo   3. git push origin main
echo.

git add .
git commit -m "%commit_msg%"
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ Изменения успешно отправлены на GitHub!
    echo.
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo 📝 СЛЕДУЮЩИЙ ШАГ: Выполните на сервере
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo.
    echo Нажмите [2] в меню для команд сервера
) else (
    echo.
    echo ❌ Ошибка при отправке изменений!
    echo Проверьте Git статус и попробуйте снова
)
echo.
pause
goto menu

:step2
cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║       ШАГ 2: КОМАНДЫ ДЛЯ СЕРВЕРА (КОПИРУЙТЕ)        ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 📋 Скопируйте и выполните на сервере:
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo # 1. Подключитесь к серверу
echo ssh root@46.62.167.17
echo.
echo # 2. Перейдите в проект и активируйте venv
echo cd /var/www/pravoslavie_portal
echo source venv/bin/activate
echo.
echo # 3. ВАЖНО: Выключите режим обслуживания (если включен)
echo python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('✅ Выключен')"
echo.
echo # 4. Выполните деплой
echo ./deploy.sh
echo.
echo # 5. Проверьте порядок middleware
echo python manage.py shell ^<^< 'PYTHON'
echo from django.conf import settings
echo ml = settings.MIDDLEWARE
echo auth_idx = ml.index('django.contrib.auth.middleware.AuthenticationMiddleware')
echo maint_idx = ml.index('core.middleware.maintenance.MaintenanceModeMiddleware')
echo print(f"Auth: {auth_idx+1}, Maint: {maint_idx+1}")
echo print("✅ OK" if maint_idx ^> auth_idx else "❌ ОШИБКА")
echo PYTHON
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 💡 ИЛИ одной командой (с вашего компьютера):
echo.
echo ssh root@46.62.167.17 -t "cd /var/www/pravoslavie_portal && source venv/bin/activate && python manage.py shell -c \"from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save()\" && ./deploy.sh"
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
goto menu

:step3
cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║         ШАГ 3: ТЕСТИРОВАНИЕ ПОСЛЕ ДЕПЛОЯ            ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 📋 Проверьте работу режима обслуживания:
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo ✅ ПРОВЕРКА 1: Включите режим через админку
echo.
echo    1. Откройте: https://dobrist.com/admin/core/sitesettings/1/change/
echo    2. Поставьте галочку "Режим обслуживания"
echo    3. Введите сообщение (опционально)
echo    4. Нажмите "Сохранить"
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo ✅ ПРОВЕРКА 2: Как администратор
echo.
echo    1. Откройте: https://dobrist.com/
echo    2. Должны увидеть:
echo       ✓ Красная полоса сверху: "РЕЖИМ ОБСЛУЖИВАНИЯ АКТИВЕН"
echo       ✓ Сайт работает нормально
echo       ✓ Кнопка "Настройки" в полосе
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo ✅ ПРОВЕРКА 3: Как обычный пользователь
echo.
echo    1. Откройте браузер в режиме инкогнито (Ctrl+Shift+N)
echo    2. Перейдите: https://dobrist.com/
echo    3. Должны увидеть:
echo       ✓ Страница обслуживания с градиентом
echo       ✓ Иконка шестеренки
echo       ✓ Ваше сообщение
echo       ✓ Кнопка "Вход для администраторов"
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo ✅ ПРОВЕРКА 4: Выключите режим
echo.
echo    1. Вернитесь в админку
echo    2. Снимите галочку "Режим обслуживания"
echo    3. Нажмите "Сохранить"
echo    4. Проверьте - сайт доступен всем
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🎉 Если все проверки прошли - система работает правильно!
echo.
pause
goto menu

:diagnostics
cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║              ДИАГНОСТИКА (КОМАНДЫ)                  ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 📋 Команды для диагностики на сервере:
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo # Проверить статус режима
echo python manage.py shell -c "from core.models import SiteSettings; print('🔴 ВКЛ' if SiteSettings.get_settings().maintenance_mode else '🟢 ВЫКЛ')"
echo.
echo # Выключить режим
echo python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('✅')"
echo.
echo # Включить режим
echo python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = True; s.save(); print('✅')"
echo.
echo # Проверить порядок middleware
echo python manage.py shell -c "from django.conf import settings; ml = settings.MIDDLEWARE; auth_idx = ml.index('django.contrib.auth.middleware.AuthenticationMiddleware'); maint_idx = ml.index('core.middleware.maintenance.MaintenanceModeMiddleware'); print('✅ OK' if maint_idx ^> auth_idx else '❌ ОШИБКА')"
echo.
echo # Проверить администраторов
echo python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); [print(f'{u.username} - super:{u.is_superuser}') for u in User.objects.filter(is_superuser=True)]"
echo.
echo # Просмотр логов
echo sudo journalctl -u gunicorn -n 50
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
goto menu

:docs
cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║                  ДОКУМЕНТАЦИЯ                       ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 📚 Доступные документы:
echo.
echo 1. CORRECT_DEPLOYMENT_GUIDE.md
echo    └─ Правильная последовательность деплоя
echo.
echo 2. URGENT_FIX.md
echo    └─ Срочное решение проблем
echo.
echo 3. MAINTENANCE_MODE_GUIDE.md
echo    └─ Полное руководство
echo.
echo 4. DEPLOY_READY.md
echo    └─ Итоговая инструкция
echo.
echo 5. MIDDLEWARE_ORDER_FIX.md
echo    └─ Объяснение порядка middleware
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🔗 Важные ссылки:
echo.
echo    Админка: https://dobrist.com/admin/
echo    Настройки: https://dobrist.com/admin/core/sitesettings/1/change/
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
goto menu

:end
cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║              🎉 УДАЧНОГО ДЕПЛОЯ!                    ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 📝 Краткая памятка:
echo.
echo    1. Локально: git add . ^&^& git commit ^&^& git push
echo    2. На сервере: ./deploy.sh
echo    3. Проверка: https://dobrist.com/admin/core/sitesettings/1/change/
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
timeout /t 3 >nul
exit
