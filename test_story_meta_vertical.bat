@echo off
echo ========================================
echo    ТЕСТ ВЕРТИКАЛЬНЫХ МЕТАДАННЫХ
echo ========================================
echo.

echo 1. Проверяем CSS стили для метаданных...
python -c "
with open('templates/stories/story_list.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Проверяем наличие ключевых CSS классов
css_elements = [
    'meta-item',
    'flex-direction: column',
    'text-align: center'
]

missing = []
for element in css_elements:
    if element not in content:
        missing.append(element)

if missing:
    print(f'❌ Отсутствуют элементы: {missing}')
else:
    print('✅ Все CSS элементы найдены')

# Проверяем HTML структуру
if 'class=\"meta-item\"' in content:
    print('✅ HTML структура обновлена')
else:
    print('❌ HTML структура не обновлена')
"

echo.
echo 2. Новая структура метаданных:
echo    👁️     📅     📁
echo просмотры  дата  категория
echo   ^^^ вертикально с иконками сверху
echo.

echo 3. Запускаем сервер для тестирования...
echo Откройте: http://127.0.0.1:8000/stories/
echo Проверьте новое расположение метаданных в карточках
echo.

python manage.py runserver 127.0.0.1:8000
