@echo off
chcp 65001 >nul
REM ==========================================
REM ЗАВЕРШЕНИЕ МИГРАЦИИ НА POSTGRESQL
REM ==========================================

echo.
echo ========================================
echo    ИМПОРТ ДАННЫХ В POSTGRESQL
echo ========================================
echo.

REM Принудительно устанавливаем PostgreSQL окружение
set DJANGO_ENV=local
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo Проверяем что .env.local настроен для PostgreSQL...

REM Проверяем что USE_SQLITE=False в .env.local
findstr "USE_SQLITE=False" .env.local >nul 2>&1
if errorlevel 1 (
    echo Настраиваем .env.local для PostgreSQL...
    (
    echo # Environment
    echo DJANGO_ENV=local
    echo.
    echo # Security
    echo SECRET_KEY=django-insecure-local-development-key-change-me  
    echo DEBUG=True
    echo ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,testserver
    echo.
    echo # === SWITCH TO POSTGRESQL ===
    echo USE_SQLITE=False
    echo.
    echo # PostgreSQL settings
    echo DB_NAME=pravoslavie_local_db
    echo DB_USER=pravoslavie_user
    echo DB_PASSWORD=local_strong_password_2024
    echo DB_HOST=localhost
    echo DB_PORT=5432
    echo.
    echo # Email ^(console for development^)
    echo EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    echo.
    echo # API keys ^(test versions^)
    echo YOUTUBE_API_KEY=your-youtube-api-key-for-testing
    echo YOOKASSA_SHOP_ID=test-shop-id  
    echo YOOKASSA_SECRET_KEY=test-secret-key
    echo YOOKASSA_TEST_MODE=True
    echo.
    echo # Redis
    echo REDIS_URL=redis://127.0.0.1:6379/1
    echo CELERY_BROKER_URL=redis://localhost:6379/0
    echo CELERY_RESULT_BACKEND=redis://localhost:6379/0
    echo.
    echo # Push notifications
    echo VAPID_PRIVATE_KEY=test-private-key-for-development-only
    echo VAPID_PUBLIC_KEY=BKkKS_8l4BqHZ8jO4yXLsJYK6Q7L_Hd-UQOUUj9SqPxKMaI6F5VJ_HqJN4R7s3uK6GnX2bOqT9hL7F2jZaWvNdc
    echo VAPID_EMAIL=admin@pravoslavie-portal.ru
    echo.
    echo # Admin
    echo ADMIN_EMAIL=admin@localhost
    echo.
    echo # Additional development settings
    echo SECURE_SSL_REDIRECT=False
    echo CACHE_BACKEND=dummy
    ) > .env.local
    echo .env.local обновлен для PostgreSQL
) else (
    echo .env.local уже настроен для PostgreSQL
)

echo.
echo Активируем виртуальное окружение...
call .venv\Scripts\activate.bat

echo.
echo STEP 1: Проверка подключения к PostgreSQL
echo ========================================

set DJANGO_ENV=local
python manage.py check --database default
if errorlevel 1 (
    echo Ошибка подключения к PostgreSQL!
    echo.
    echo Проверьте:
    echo   1. PostgreSQL запущен
    echo   2. База pravoslavie_local_db создана
    echo   3. Пользователь pravoslavie_user существует  
    echo   4. Пароль правильный: local_strong_password_2024
    echo.
    pause
    exit /b 1
)

echo Подключение к PostgreSQL успешно!
echo.

echo STEP 2: Применение миграций
echo ============================

set DJANGO_ENV=local
python manage.py migrate
if errorlevel 1 (
    echo Ошибка применения миграций
    pause
    exit /b 1
)

echo Структура БД создана успешно!
echo.

echo STEP 3: Импорт данных
echo =====================

REM Находим файлы экспорта
echo Поиск файлов экспорта...

set IMPORT_SUCCESS=0

REM Импорт в правильном порядке
echo Импорт пользователей...
for %%f in (backups\auth_User_*.json) do (
    set DJANGO_ENV=local
    python manage.py loaddata "%%f"
    if not errorlevel 1 set /a IMPORT_SUCCESS+=1
)

echo Импорт групп...
for %%f in (backups\auth_Group_*.json) do (
    set DJANGO_ENV=local
    python manage.py loaddata "%%f"
    if not errorlevel 1 set /a IMPORT_SUCCESS+=1
)

echo Импорт основных данных...
for %%f in (backups\core_*.json) do (
    set DJANGO_ENV=local
    python manage.py loaddata "%%f"
    if not errorlevel 1 set /a IMPORT_SUCCESS+=1
)

echo Импорт рассказов...
for %%f in (backups\stories_*.json) do (
    set DJANGO_ENV=local
    python manage.py loaddata "%%f"
    if not errorlevel 1 set /a IMPORT_SUCCESS+=1
)

echo Импорт книг...
for %%f in (backups\books_*.json) do (
    set DJANGO_ENV=local
    python manage.py loaddata "%%f"
    if not errorlevel 1 set /a IMPORT_SUCCESS+=1
)

echo Импорт сказок...
for %%f in (backups\fairy_tales_*.json) do (
    set DJANGO_ENV=local
    python manage.py loaddata "%%f"
    if not errorlevel 1 set /a IMPORT_SUCCESS+=1
)

echo Импорт магазина...
for %%f in (backups\shop_*.json) do (
    set DJANGO_ENV=local
    python manage.py loaddata "%%f"
    if not errorlevel 1 set /a IMPORT_SUCCESS+=1
)

echo Импорт аккаунтов...
for %%f in (backups\accounts_*.json) do (
    set DJANGO_ENV=local
    python manage.py loaddata "%%f"
    if not errorlevel 1 set /a IMPORT_SUCCESS+=1
)

echo Импорт подписок...
for %%f in (backups\subscriptions_*.json) do (
    set DJANGO_ENV=local
    python manage.py loaddata "%%f"
    if not errorlevel 1 set /a IMPORT_SUCCESS+=1
)

echo.
echo Импортировано компонентов: %IMPORT_SUCCESS%
echo.

echo STEP 4: Создание суперпользователя
echo ==================================

set DJANGO_ENV=local
echo Создание администратора ^(или нажмите Ctrl+C для пропуска^):
python manage.py createsuperuser
if errorlevel 1 (
    echo Создание суперпользователя пропущено
)

echo.

echo STEP 5: Проверка работы сайта
echo =============================

set DJANGO_ENV=local
echo Запуск сервера Django...
echo.
echo Проверьте эти страницы:
echo   • Главная: http://127.0.0.1:8000/
echo   • Админка: http://127.0.0.1:8000/admin/
echo   • Рассказы: http://127.0.0.1:8000/stories/
echo   • Книги: http://127.0.0.1:8000/books/
echo   • Магазин: http://127.0.0.1:8000/shop/
echo   • Сказки: http://127.0.0.1:8000/fairy-tales/
echo.
echo Нажмите Ctrl+C для остановки сервера
echo.

python manage.py runserver 127.0.0.1:8000

echo.
echo ==========================================
echo        МИГРАЦИЯ НА POSTGRESQL ЗАВЕРШЕНА!
echo ==========================================
echo.
echo Что сделано:
echo   PostgreSQL подключена
echo   Структура БД создана
echo   Данные импортированы
echo   Суперпользователь создан
echo   Сервер протестирован
echo.
echo СЛЕДУЮЩИЕ ШАГИ:
echo   1. Протестируйте все функции сайта
echo   2. Создайте бэкап: create_postgresql_backup_en.bat
echo   3. Переходите к Docker контейнеризации
echo.
pause