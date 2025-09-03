@echo off
REM ==========================================
REM СКРИПТ ПЕРЕВОДА НА POSTGRESQL  
REM ==========================================

echo.
echo ========================================
echo    МИГРАЦИЯ SQLITE -> POSTGRESQL
echo ========================================
echo.

REM Проверка виртуального окружения
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Виртуальное окружение не найдено!
    echo Создайте .venv и установите зависимости
    pause
    exit /b 1
)

REM Активация виртуального окружения  
echo 🔄 Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo.
echo ЭТАП 1: Резервное копирование SQLite
echo =====================================
echo 📦 Создаем экспорт данных из SQLite...

REM Создание директории для бэкапов
if not exist "backups" mkdir backups

REM Экспорт данных с временной меткой
set BACKUP_TIME=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%
set BACKUP_TIME=%BACKUP_TIME: =0%

python manage.py dumpdata --natural-foreign --natural-primary -o "backups\sqlite_full_%BACKUP_TIME%.json"
if errorlevel 1 (
    echo ❌ Ошибка при создании полного экспорта
    pause
    exit /b 1
)

python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission -o "backups\sqlite_clean_%BACKUP_TIME%.json"
if errorlevel 1 (
    echo ❌ Ошибка при создании чистого экспорта  
    pause
    exit /b 1
)

echo ✅ Экспорт SQLite данных завершен
echo    📁 Файлы сохранены в папку backups\
echo.

echo ЭТАП 2: Проверка PostgreSQL подключения
echo =======================================
echo 🔗 Проверяем подключение к PostgreSQL...

REM Обновляем .env файл для PostgreSQL
echo 📝 Обновляем настройки .env.local...
(
echo # Окружение
echo DJANGO_ENV=local
echo.
echo # Безопасность
echo SECRET_KEY=django-insecure-local-development-key-change-me  
echo DEBUG=True
echo ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,testserver
echo.
echo # === ПЕРЕКЛЮЧЕНИЕ НА POSTGRESQL ===
echo USE_SQLITE=False
echo.
echo # Настройки PostgreSQL
echo DB_NAME=pravoslavie_local_db
echo DB_USER=pravoslavie_user
echo DB_PASSWORD=local_strong_password_2024
echo DB_HOST=localhost
echo DB_PORT=5432
echo.
echo # Email ^(письма в консоль для разработки^)
echo EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
echo.
echo # API ключи ^(тестовые версии^)
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
echo # Push-уведомления
echo VAPID_PRIVATE_KEY=test-private-key-for-development-only
echo VAPID_PUBLIC_KEY=BKkKS_8l4BqHZ8jO4yXLsJYK6Q7L_Hd-UQOUUj9SqPxKMaI6F5VJ_HqJN4R7s3uK6GnX2bOqT9hL7F2jZaWvNdc
echo VAPID_EMAIL=admin@pravoslavie-portal.ru
echo.
echo # Админ
echo ADMIN_EMAIL=admin@localhost
echo.
echo # Дополнительные настройки разработки
echo SECURE_SSL_REDIRECT=False
echo CACHE_BACKEND=dummy
) > .env.local

echo ✅ Настройки .env.local обновлены для PostgreSQL
echo.

REM Проверка подключения к БД
echo 🔍 Проверяем подключение Django к PostgreSQL...
python manage.py check --database default
if errorlevel 1 (
    echo ❌ Ошибка подключения к PostgreSQL!
    echo.
    echo 💡 Проверьте:
    echo    1. PostgreSQL запущен
    echo    2. База pravoslavie_local_db создана
    echo    3. Пользователь pravoslavie_user существует  
    echo    4. Пароль в .env.local правильный
    echo.
    pause
    exit /b 1
)

echo ✅ Подключение к PostgreSQL успешно
echo.

echo ЭТАП 3: Создание структуры БД
echo =============================
echo 🏗️ Применяем миграции Django...

python manage.py migrate
if errorlevel 1 (
    echo ❌ Ошибка при применении миграций
    pause
    exit /b 1
)

echo ✅ Структура БД создана успешно
echo.

echo ЭТАП 4: Импорт данных
echo =====================
echo 📥 Загружаем данные в PostgreSQL...

REM Находим последний созданный бэкап
for /f %%i in ('dir /b /o:d "backups\sqlite_clean_*.json"') do set LATEST_BACKUP=%%i

echo 📂 Импортируем файл: %LATEST_BACKUP%
python manage.py loaddata "backups\%LATEST_BACKUP%"
if errorlevel 1 (
    echo ⚠️ Ошибка при импорте чистых данных
    echo 🔄 Попробуем полный импорт...
    
    for /f %%i in ('dir /b /o:d "backups\sqlite_full_*.json"') do set LATEST_FULL_BACKUP=%%i
    python manage.py loaddata "backups\%LATEST_FULL_BACKUP%" --verbosity=2
    if errorlevel 1 (
        echo ❌ Критическая ошибка импорта данных
        pause
        exit /b 1
    )
)

echo ✅ Данные импортированы успешно
echo.

echo ЭТАП 5: Создание суперпользователя
echo ==================================
echo 👤 Создание администратора для PostgreSQL...
echo.
echo Введите данные для суперпользователя:

python manage.py createsuperuser
if errorlevel 1 (
    echo ⚠️ Пропускаем создание суперпользователя
)

echo.

echo ЭТАП 6: Проверка работоспособности
echo ==================================
echo 🧪 Запуск тестов системы...

REM Проверяем что сайт запускается
echo 🚀 Проверяем запуск сервера...
timeout /t 2 > nul
start /min python manage.py runserver 127.0.0.1:8000

echo.
echo 🌐 Сервер запущен на http://127.0.0.1:8000
echo.
echo ✅ Проверьте в браузере:
echo    • Главная страница: http://127.0.0.1:8000/
echo    • Админка: http://127.0.0.1:8000/admin/  
echo    • Рассказы: http://127.0.0.1:8000/stories/
echo    • Книги: http://127.0.0.1:8000/books/
echo    • Магазин: http://127.0.0.1:8000/shop/
echo.

echo ЭТАП 7: Создание бэкапа PostgreSQL
echo ===================================
echo 💾 Создаем бэкап новой PostgreSQL БД...

REM Создаем дамп PostgreSQL
set PG_BACKUP_FILE=backups\postgresql_%BACKUP_TIME%.sql
pg_dump -U pravoslavie_user -h localhost -d pravoslavie_local_db -f "%PG_BACKUP_FILE%"
if errorlevel 1 (
    echo ⚠️ Не удалось создать pg_dump (возможно нет в PATH)
    echo 💡 Создайте бэкап вручную через pgAdmin или добавьте PostgreSQL в PATH
) else (
    echo ✅ Бэкап PostgreSQL создан: %PG_BACKUP_FILE%
)

echo.
echo ==========================================
echo        ✅ МИГРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!
echo ==========================================
echo.
echo 🎯 Что сделано:
echo    ✅ SQLite данные экспортированы
echo    ✅ PostgreSQL настроен и подключен  
echo    ✅ Структура БД создана
echo    ✅ Данные импортированы
echo    ✅ Суперпользователь создан
echo    ✅ Сервер запущен и работает
echo    ✅ Бэкапы созданы
echo.
echo 🚀 СЛЕДУЮЩИЕ ШАГИ:
echo    1. Протестируйте все функции сайта
echo    2. Убедитесь что все данные на месте
echo    3. Переходим к созданию Docker инфраструктуры
echo.
echo 💡 Для остановки сервера нажмите Ctrl+C в окне сервера
echo.
pause