@echo off
echo 🛒 ПРОВЕРКА ИСПРАВЛЕНИЙ КНОПКИ ПОКУПКИ В ИЗБРАННОМ
echo ======================================================

cd /d "E:\pravoslavie_portal"

echo.
echo 📍 Текущая директория: %CD%

echo.
echo 1️⃣ Проверяем, что ссылка заменена на кнопку...
findstr /n "shop:catalog" templates\books\user_favorites.html
if %errorlevel%==0 (
    echo ❌ НАЙДЕНЫ СТАРЫЕ ССЫЛКИ НА МАГАЗИН!
) else (
    echo ✅ Старые ссылки удалены
)

echo.
echo 2️⃣ Проверяем новые кнопки...
findstr /n "btn-add-to-cart-favorites" templates\books\user_favorites.html
if %errorlevel%==0 (
    echo ✅ Новые кнопки найдены
) else (
    echo ❌ Новые кнопки НЕ найдены!
)

echo.
echo 3️⃣ Проверяем JavaScript...
findstr /n "btn-add-to-cart-favorites" templates\books\user_favorites.html
if %errorlevel%==0 (
    echo ✅ JavaScript обработчик найден
) else (
    echo ❌ JavaScript обработчик НЕ найден!
)

echo.
echo 4️⃣ Сборка статических файлов...
python manage.py collectstatic --noinput

echo.
echo 🎯 ИНСТРУКЦИИ ДЛЯ ТЕСТИРОВАНИЯ:
echo 1. Запустите сервер: python manage.py runserver
echo 2. Добавьте платные книги в избранное
echo 3. Перейдите: http://127.0.0.1:8000/books/favorites/
echo 4. Нажмите кнопку "Купить за X ₽"
echo 5. Проверьте:
echo    - Появилось ли уведомление
echo    - Обновился ли счетчик корзины
echo    - Изменилась ли кнопка на "Перейти в корзину"

echo.
echo 🔍 ОТЛАДКА:
echo - Откройте консоль браузера (F12)
echo - Проверьте ошибки JavaScript
echo - Убедитесь, что запрос идет на /shop/add-book-to-cart/

echo.
echo 🎉 ГОТОВО! Если тест показал ✅, то исправления применены!

pause
