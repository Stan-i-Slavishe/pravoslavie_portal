@echo off
echo Обновляем статические файлы...
python manage.py collectstatic --noinput --clear
echo.
echo Статические файлы обновлены!
echo.
echo Теперь обновите страницу в браузере (Ctrl+F5)
echo Кнопка избранного должна стать золотистой!
echo.
pause
