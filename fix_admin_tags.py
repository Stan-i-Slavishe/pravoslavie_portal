"""
Временное решение для отображения тегов в админке
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def fix_admin_tags():
    """Изменяем настройки админки для отображения тегов"""
    
    print("\n" + "=" * 70)
    print("ПРИМЕНЕНИЕ ВРЕМЕННОГО РЕШЕНИЯ")
    print("=" * 70)
    
    admin_file = "E:\\pravoslavie_portal\\stories\\admin.py"
    
    # Читаем файл
    with open(admin_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем текущее состояние
    if "filter_horizontal = ['tags']" in content:
        print("\n✅ Найдена строка: filter_horizontal = ['tags']")
        
        choice = input("\nИзменить на обычный виджет выбора? (y/n): ")
        
        if choice.lower() == 'y':
            # Комментируем строку
            content = content.replace(
                "filter_horizontal = ['tags']",
                "# filter_horizontal = ['tags']  # Временно отключено для отладки"
            )
            
            # Сохраняем
            with open(admin_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("\n✅ Изменения применены!")
            print("Теперь теги будут отображаться как обычный список множественного выбора.")
            print("\nПерезапустите сервер:")
            print("  python manage.py runserver")
        else:
            print("\nОтменено.")
    
    elif "# filter_horizontal = ['tags']" in content:
        print("\n⚠️ filter_horizontal уже закомментирован")
        
        choice = input("\nВернуть обратно горизонтальный фильтр? (y/n): ")
        
        if choice.lower() == 'y':
            # Раскомментируем
            content = content.replace(
                "# filter_horizontal = ['tags']",
                "filter_horizontal = ['tags']"
            )
            
            # Сохраняем
            with open(admin_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("\n✅ Горизонтальный фильтр восстановлен!")
            print("\nПерезапустите сервер:")
            print("  python manage.py runserver")
    else:
        print("\n❌ Не найдена строка filter_horizontal в admin.py")

if __name__ == '__main__':
    fix_admin_tags()
