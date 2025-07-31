#!/usr/bin/env python
"""
Экстренное исправление проблемы с невидимой кнопкой покупки
"""

def add_emergency_css_to_base():
    """Добавляет экстренные CSS-стили прямо в base.html"""
    
    base_template_path = 'E:/pravoslavie_portal/templates/base.html'
    
    # CSS для принудительного отображения кнопки
    emergency_css = '''
    <!-- ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ КНОПКИ ПОКУПКИ -->
    <style>
        /* Принудительное отображение кнопки покупки */
        .btn-purchase {
            display: inline-flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            background: linear-gradient(135deg, #d4af37, #b8941f) !important;
            border: none !important;
            color: white !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            text-decoration: none !important;
            align-items: center !important;
            gap: 8px !important;
            width: auto !important;
            height: auto !important;
            margin: 5px 0 !important;
            z-index: 9999 !important;
            position: relative !important;
            font-size: 14px !important;
        }

        .btn-purchase:hover {
            background: linear-gradient(135deg, #b8941f, #d4af37) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3) !important;
            color: white !important;
            text-decoration: none !important;
        }

        /* Принудительное отображение блока кнопок */
        .book-actions {
            display: flex !important;
            flex-direction: column !important;
            gap: 10px !important;
            margin: 1.5rem 0 !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

        .book-actions > * {
            display: inline-flex !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

        /* Отладочная рамка для кнопки покупки */
        .btn-purchase {
            border: 2px solid red !important;
            background: #ff6b6b !important;
        }
        
        .btn-purchase::before {
            content: "ТЕСТ КНОПКИ: " !important;
            color: white !important;
            font-weight: bold !important;
        }
    </style>
    '''
    
    try:
        # Читаем файл
        with open(base_template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ищем место для вставки (после существующих стилей)
        insert_position = content.find('<!-- Дополнительные стили -->')
        
        if insert_position == -1:
            # Ищем альтернативное место
            insert_position = content.find('{% block extra_css %}')
            if insert_position == -1:
                insert_position = content.find('</head>')
        
        if insert_position != -1:
            # Вставляем CSS перед найденной позицией
            new_content = content[:insert_position] + emergency_css + '\\n\\n    ' + content[insert_position:]
            
            # Создаем резервную копию
            backup_path = base_template_path + '.emergency_backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Создана резервная копия: {backup_path}")
            
            # Записываем исправленный файл
            with open(base_template_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Экстренный CSS добавлен в base.html")
            print("🔧 Кнопка покупки теперь будет видна с красной рамкой!")
            print("🚀 Перезапустите сервер Django для применения изменений")
            
            return True
        else:
            print("❌ Не удалось найти место для вставки CSS")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == '__main__':
    print("🚨 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ НЕВИДИМОЙ КНОПКИ ПОКУПКИ")
    print("=" * 60)
    
    if add_emergency_css_to_base():
        print("\\n✅ Исправление применено!")
        print("\\n📋 СЛЕДУЮЩИЕ ШАГИ:")
        print("   1. Перезапустите сервер Django")
        print("   2. Обновите страницу книги (Ctrl+F5)")
        print("   3. Кнопка покупки должна появиться с красной рамкой")
        print("   4. После подтверждения работы удалите отладочные стили")
    else:
        print("\\n❌ Исправление не удалось.")
