@echo off
echo 🎯 БЫСТРОЕ РЕШЕНИЕ: Переносим счетчик под кнопки
echo.

echo 📝 Применяем минимальные изменения к существующему файлу...

echo ✅ Изменения:
echo - Счетчик перенесен в строку с кнопками
echo - Компактный формат: 0/1000
echo - Сохранена вся функциональность
echo.

python -c "
import re

# Читаем файл
with open('comments/templates/comments/comments_section.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Убираем старый счетчик под полем ввода
old_counter = '''                            <div class=\"form-text counter-hide-mobile d-none d-md-block\">
                                <span id=\"char-counter\">0</span>/1000 символов
                            </div>'''

# Ищем и заменяем блок с кнопками
old_buttons = '''                        <div class=\"d-flex justify-content-between\">
                            <div>
                                <button type=\"submit\" class=\"btn btn-primary\" id=\"submit-comment\">
                                    <i class=\"bi bi-send me-1\"></i>
                                    Опубликовать
                                </button>
                                <button type=\"button\" class=\"btn btn-secondary ms-2\" id=\"cancel-comment\">
                                    Отмена
                                </button>
                            </div>
                            <small class=\"text-muted align-self-center\">
                                Ctrl+Enter для быстрой отправки
                            </small>
                        </div>'''

new_buttons = '''                        <div class=\"d-flex justify-content-between align-items-center flex-wrap\">
                            <div class=\"mb-2 mb-sm-0\">
                                <button type=\"submit\" class=\"btn btn-primary\" id=\"submit-comment\">
                                    <i class=\"bi bi-send me-1\"></i>
                                    <span class=\"d-none d-sm-inline\">Опубликовать</span>
                                    <span class=\"d-sm-none\">Отправить</span>
                                </button>
                                <button type=\"button\" class=\"btn btn-secondary ms-2\" id=\"cancel-comment\">
                                    <span class=\"d-none d-sm-inline\">Отмена</span>
                                    <span class=\"d-sm-none\">×</span>
                                </button>
                            </div>
                            <div class=\"d-flex flex-column align-items-end\">
                                <small class=\"text-muted d-none d-lg-block mb-1\" style=\"font-size: 11px;\">
                                    Ctrl+Enter
                                </small>
                                <div class=\"text-muted\" style=\"font-size: 13px;\">
                                    <span id=\"char-counter\">0</span><span class=\"text-muted\">/1000</span>
                                </div>
                            </div>
                        </div>'''

# Заменяем старый счетчик на пустую строку
content = content.replace(old_counter, '')

# Заменяем кнопки
content = content.replace(old_buttons, new_buttons)

# Обновляем CSS для лучшего отображения на мобильных
css_addition = '''
/* Адаптивный счетчик */
@media (max-width: 480px) {
    .d-flex.justify-content-between.align-items-center.flex-wrap {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 10px;
    }
    
    .d-flex.flex-column.align-items-end {
        align-items: center !important;
    }
}

#char-counter {
    font-weight: 600;
    transition: color 0.3s ease;
}

#char-counter.warning {
    color: #f57c00 !important;
}

#char-counter.danger {
    color: #dc3545 !important;
    animation: pulse 1s infinite;
}'''

# Добавляем CSS перед закрывающим тегом </style>
content = content.replace('</style>', css_addition + '\n</style>')

# Сохраняем файл
with open('comments/templates/comments/comments_section.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Файл успешно обновлен!')
"

if %errorlevel% neq 0 (
    echo ❌ Ошибка при обновлении файла
    pause
    exit /b 1
)

echo.
echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

echo.
echo 🎯 ГОТОВО! Изменения:
echo - ✅ Счетчик теперь справа от кнопок
echo - ✅ Компактный формат: 0/1000  
echo - ✅ Адаптивные кнопки для мобильных
echo - ✅ На маленьких экранах счетчик под кнопками
echo.

echo 🚀 Перезапустите сервер и проверьте!
echo python manage.py runserver
echo.

pause
