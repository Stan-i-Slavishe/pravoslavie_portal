@echo off
echo Добавляем тег "дочь" к тестовой истории...
echo.

cd /d "E:\pravoslavie_portal"
python add_test_tag.py

echo.
echo Готово! Проверьте результат на странице: http://127.0.0.1:8000/tags/doch/
pause
