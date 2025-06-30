@echo off
echo ===== ЗАПУСК INLINE-ОТВЕТОВ КАК НА YOUTUBE =====
echo.

echo 🎯 ОСНОВНАЯ ЗАДАЧА ВЫПОЛНЕНА!
echo ✅ Создана система inline-ответов
echo 📝 JavaScript для YouTube-стиля готов
echo.

echo 🔄 Собираем статические файлы...
python manage.py collectstatic --noinput --clear

echo.
echo 🚀 Запускаем сервер с новой функциональностью...
echo 💡 Теперь когда вы нажмете "Ответить" на любой комментарий:
echo    - Форма появится ПРЯМО ПОД комментарием
echo    - Как на YouTube!
echo    - С анимацией и счетчиком символов
echo.

start http://127.0.0.1:8000/stories/pasha-voskresenie-hristovo/
python manage.py runserver
