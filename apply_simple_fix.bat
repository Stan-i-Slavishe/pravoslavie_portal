@echo off
echo 🔧 Применяем простое решение - скрытие счетчика на мобильных...
echo.

echo ✅ Изменения применены:
echo - Счетчик будет скрыт на экранах меньше 768px  
echo - На десктопе работает как обычно
echo.

echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

echo.
echo ✨ Готово! Теперь счетчик символов:
echo - 💻 Видим на десктопе
echo - 📱 Скрыт на мобильных
echo.

echo 🎯 Перезапустите сервер и проверьте:
echo python manage.py runserver
echo.

pause
