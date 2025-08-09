#!/usr/bin/env python
"""
Быстрое исправление персонализированных сказок
"""

import os
import sys
import django

# Добавляем путь к проекту
project_path = 'E:/pravoslavie_portal'
if project_path not in sys.path:
    sys.path.append(project_path)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product

def fix_fairy_tales():
    """Исправляем настройки персонализации для сказок"""
    
    print("🔧 Исправляем персонализированные сказки...")
    
    # Находим все сказки
    fairy_tales = Product.objects.filter(
        product_type='fairy_tale',
        is_active=True
    )
    
    print(f"📚 Найдено сказок: {fairy_tales.count()}")
    
    fixed_count = 0
    
    for tale in fairy_tales:
        print(f"\n📖 Сказка: {tale.title}")
        print(f"   Требует персонализации: {tale.requires_personalization}")
        
        if not tale.requires_personalization:
            print("   🔧 ИСПРАВЛЯЕМ: Устанавливаем requires_personalization=True")
            tale.requires_personalization = True
            tale.save()
            fixed_count += 1
            print("   ✅ ИСПРАВЛЕНО!")
        else:
            print("   ✅ Уже настроено правильно")
    
    print(f"\n🎉 Исправлено сказок: {fixed_count}")
    print("Перезагрузите страницу каталога для проверки!")

if __name__ == "__main__":
    fix_fairy_tales()
