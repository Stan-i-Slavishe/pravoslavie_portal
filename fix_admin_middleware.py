# Скрипт для исправления проблем с админкой
# Временно отключает проблемные middleware

import os
import re

def fix_admin_middleware():
    """Исправляет проблемы с админкой, отключая проблемные middleware"""
    
    settings_path = "E:\\pravoslavie_portal\\config\\settings.py"
    
    # Читаем текущие настройки
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Комментируем проблемные middleware
    problematic_middleware = [
        'stories.middleware.AdminPerformanceMiddleware',
        'stories.middleware.DatabaseOptimizationMiddleware',
    ]
    
    for middleware in problematic_middleware:
        # Ищем строку с middleware и комментируем её
        pattern = f"^(\s*)'{middleware}',?\s*$"
        replacement = r"\1# '\g<0>'  # 🚫 ВРЕМЕННО ОТКЛЮЧЕН ДЛЯ ИСПРАВЛЕНИЯ АДМИНКИ"
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Записываем исправленные настройки
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Проблемные middleware отключены!")
    print("📋 Отключены:")
    for middleware in problematic_middleware:
        print(f"   - {middleware}")
    
    print("\n🔄 Перезапустите сервер для применения изменений:")
    print("   python manage.py runserver")

if __name__ == "__main__":
    fix_admin_middleware()
