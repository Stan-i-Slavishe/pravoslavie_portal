@echo off
chcp 65001 >nul
echo ===============================================
echo 🧚 ВОССТАНОВЛЕНИЕ СИСТЕМЫ ТЕРАПЕВТИЧЕСКИХ СКАЗОК
echo ===============================================
echo.

echo 📝 Шаг 1: Копируем новые views...
copy /Y restored_views.py fairy_tales\views.py
if %errorlevel% == 0 (
    echo ✅ Views обновлены
) else (
    echo ❌ Ошибка копирования views
    pause
    exit /b 1
)

echo.
echo 📝 Шаг 2: Копируем новые URLs...
copy /Y restored_urls.py fairy_tales\urls.py
if %errorlevel% == 0 (
    echo ✅ URLs обновлены
) else (
    echo ❌ Ошибка копирования URLs
    pause
    exit /b 1
)

echo.
echo 📝 Шаг 3: Применяем миграции...
python manage.py makemigrations fairy_tales
python manage.py migrate
if %errorlevel% == 0 (
    echo ✅ Миграции применены
) else (
    echo ❌ Ошибка применения миграций
    pause
    exit /b 1
)

echo.
echo 📝 Шаг 4: Создаем тестовые данные...
python create_fairy_tales_data.py
if %errorlevel% == 0 (
    echo ✅ Тестовые данные созданы
) else (
    echo ❌ Ошибка создания тестовых данных
    pause
    exit /b 1
)

echo.
echo 📝 Шаг 5: Собираем статические файлы...
python manage.py collectstatic --noinput
if %errorlevel% == 0 (
    echo ✅ Статические файлы собраны
) else (
    echo ❌ Ошибка сборки статических файлов
    echo ⚠️  Продолжаем без критической ошибки...
)

echo.
echo ===============================================
echo ✅ СИСТЕМА СКАЗОК УСПЕШНО ВОССТАНОВЛЕНА!
echo ===============================================
echo.
echo 🌟 Теперь доступно:
echo   • Каталог сказок: /fairy-tales/
echo   • Категории: /fairy-tales/categories/
echo   • Персонализация сказок
echo   • Система избранного
echo   • Отзывы и рейтинги
echo   • Заказы персонализации
echo.
echo 📚 Созданные категории:
echo   • Преодоление страхов
echo   • Повышение уверенности  
echo   • Улучшение отношений
echo   • Коррекция поведения
echo   • Управление эмоциями
echo   • Духовное воспитание
echo.
echo 🚀 Запустите сервер: python manage.py runserver
echo 🌐 Перейдите на: http://127.0.0.1:8000/fairy-tales/
echo.
pause
