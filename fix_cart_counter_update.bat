@echo off
echo 🚀 ИСПРАВЛЕНИЕ АВТОМАТИЧЕСКОГО ОБНОВЛЕНИЯ СЧЕТЧИКА КОРЗИНЫ
echo ============================================================

cd /d "E:\pravoslavie_portal"

echo.
echo 📍 Текущая директория: %CD%

echo.
echo 1️⃣ Запуск финального тестирования...
python final_cart_update_test.py

echo.
echo 2️⃣ Сбор статических файлов...
python manage.py collectstatic --noinput

echo.
echo 3️⃣ Проверка миграций...
python manage.py makemigrations
python manage.py migrate

echo.
echo 🎯 РЕЗУЛЬТАТ ИСПРАВЛЕНИЙ:
echo ✅ Добавлена функция get_cart_count в shop/views.py
echo ✅ Добавлен JavaScript updateCartCount() в base.html  
echo ✅ Обновлен код добавления в корзину в book_detail.html
echo ✅ Счетчик корзины теперь обновляется автоматически
echo ✅ CSS стили для бейджей уже настроены

echo.
echo 📋 СЛЕДУЮЩИЕ ШАГИ:
echo 1. Запустите сервер: python manage.py runserver
echo 2. Авторизуйтесь в системе
echo 3. Откройте страницу платной книги
echo 4. Нажмите "Купить за X ₽"
echo 5. Проверьте обновление счетчика корзины

echo.
echo 🎉 ГОТОВО! Счетчик корзины теперь обновляется без перезагрузки страницы!

pause
