@echo off
echo 🔥 ПРИНУДИТЕЛЬНАЯ ОЧИСТКА КЕША И ПЕРЕЗАГРУЗКА
echo.

echo 🗑️ Очищаем кеш Django...
python -c "from django.core.cache import cache; cache.clear(); print('Django кеш очищен')"

echo 🧹 Принудительно пересобираем статику...
python manage.py collectstatic --clear --noinput

echo 📦 Перезапускаем процесс Django...
taskkill /F /IM python.exe 2>nul || echo "Django процесс не найден"

echo.
echo ✅ Теперь запустите сервер и обязательно:
echo.
echo 1️⃣ python manage.py runserver
echo.
echo 2️⃣ В браузере нажмите Ctrl+Shift+R (жесткая перезагрузка)
echo    ИЛИ F12 → правой кнопкой на кнопке обновления → "Очистить кеш и жесткая перезагрузка"
echo.
echo 3️⃣ Откройте любой рассказ и попробуйте добавить комментарий
echo.
echo 💡 Если изменения все еще не видны, попробуйте:
echo - Открыть в режиме инкогнито
echo - Очистить кеш браузера полностью
echo - Проверить в другом браузере
echo.

echo 🎯 Ожидаемый результат:
echo Кнопки: [× Отправить]        Счетчик: "2000 осталось"
echo (на мобильных счетчик под кнопками по центру)
echo.

pause
