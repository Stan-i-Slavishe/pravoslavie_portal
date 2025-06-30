#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 ИСПРАВЛЕНИЕ SETTINGS.PY - УДАЛЕНИЕ COMMENTS
"""

def fix_settings():
    print("🔧 ИСПРАВЛЕНИЕ config/settings.py")
    print("=" * 40)
    
    settings_file = 'config/settings.py'
    
    try:
        # Читаем файл
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📄 Читаем settings.py...")
        
        # Удаляем 'comments' из LOCAL_APPS
        old_line = "    'comments',       # система комментариев"
        new_content = content.replace(old_line, "")
        
        # Также удаляем если есть просто 'comments',
        new_content = new_content.replace("    'comments',\n", "")
        
        # Записываем исправленный файл
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Удален 'comments' из INSTALLED_APPS")
        print("✅ Файл config/settings.py исправлен")
        
    except FileNotFoundError:
        print(f"❌ Файл {settings_file} не найден")
    except Exception as e:
        print(f"💥 Ошибка: {e}")

if __name__ == "__main__":
    fix_settings()
