@echo off
echo =================================
echo 🔧 ТЕСТИРОВАНИЕ ВЕРТИКАЛЬНОГО ИСПРАВЛЕНИЯ ПЛЕЙЛИСТА
echo =================================
echo.

echo ✅ Применено ВЕРТИКАЛЬНОЕ исправление:
echo    - flex-direction: column для .playlist-meta
echo    - Каждый элемент метаданных на отдельной строке
echo    - width: 100%% для полной ширины элементов
echo    - Центрирование содержимого
echo    - Улучшенные отступы и padding
echo.

echo 📱 Проверьте в мобильном режиме:
echo    1. F12 -> Device Toggle (Ctrl+Shift+M)
echo    2. iPhone SE (375px)
echo    3. Перейдите на плейлист
echo.

echo 🎯 Ожидаемый результат:
echo    - Количество рассказов    (строка 1)
echo    - Дата создания           (строка 2)  
echo    - Статус приватности      (строка 3)
echo    - Все элементы центрированы по горизонтали
echo    - Никаких наложений и сжатий
echo.

echo 🚀 Запускаем тест...
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    python manage.py runserver 127.0.0.1:8000
) else (
    echo ❌ Виртуальное окружение не найдено!
    pause
)
