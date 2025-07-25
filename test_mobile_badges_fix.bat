@echo off
echo =================================
echo ТЕСТ: Исправление позиционирования бейджей в мобильной версии
echo =================================

echo.
echo Изменения:
echo 1. Убраны Bootstrap классы position-absolute, top-0, start-100, translate-middle
echo 2. Добавлено точное CSS позиционирование с position: absolute
echo 3. Настроена адаптивность для разных размеров экранов:
echo    - Десктоп: top: -6px, right: -8px
echo    - Планшеты (768px): top: -4px, right: -6px  
echo    - Мобильные (576px): top: -3px, right: -5px
echo 4. Добавлен position: relative для .nav-link родительского элемента

echo.
echo Запуск сервера для тестирования...
echo Откройте браузер в режиме мобильного устройства (F12 -> Device Mode)
echo Проверьте страницу http://127.0.0.1:8000/books/
echo.

cd /d "E:\pravoslavie_portal"
python manage.py runserver 127.0.0.1:8000
