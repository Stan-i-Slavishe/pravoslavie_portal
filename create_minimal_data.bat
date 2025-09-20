@echo off
echo 🎯 СОЗДАНИЕ МИНИМАЛЬНЫХ ТЕСТОВЫХ ДАННЫХ ДЛЯ SEO РАБОТЫ
echo ====================================================

echo 🎲 Создаем тестовые данные...
python create_test_data.py

echo.
echo ✅ Тестовые данные созданы!
echo.
echo 📊 Проверим что получилось:
python manage.py shell -c "
from stories.models import Story; 
from core.models import Category, Tag; 
from books.models import Book;
print(f'Рассказы: {Story.objects.count()}');
print(f'Категории: {Category.objects.count()}');
print(f'Теги: {Tag.objects.count()}');
print(f'Книги: {Book.objects.count()}');
"

echo.
echo 🚀 Запустите сервер и проверьте сайт:
echo python manage.py runserver

echo.
echo 🎯 После проверки сайта продолжим с SEO оптимизацией для dobrist.com

pause
