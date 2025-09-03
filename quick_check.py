#!/usr/bin/env python3
"""
🔍 Быстрая проверка после очистки
"""

import os
import subprocess
import sys

def quick_check():
    print("🔍 БЫСТРАЯ ПРОВЕРКА ПОСЛЕ ОЧИСТКИ")
    print("=" * 50)
    
    # Проверяем .env файлы
    print("\n📁 Проверка .env файлов:")
    env_files = [f for f in os.listdir('.') if f.startswith('.env') and not f.startswith('.env.')]
    
    should_exist = ['.env.local', '.env.staging', '.env.production']
    should_not_exist = ['.env', '.env.lightweight', '.env.postgres_local', '.env.push_test', '.env.temp']
    
    all_good = True
    
    for file_name in should_exist:
        if os.path.exists(file_name):
            print(f"✅ {file_name} - найден")
        else:
            print(f"❌ {file_name} - НЕ НАЙДЕН!")
            all_good = False
    
    for file_name in should_not_exist:
        if os.path.exists(file_name):
            print(f"⚠️ {file_name} - всё ещё существует (нужно удалить)")
            all_good = False
        else:
            print(f"✅ {file_name} - удален")
    
    # Тест Django
    print(f"\n🧪 Тестирование Django:")
    try:
        os.environ['DJANGO_ENV'] = 'local'
        result = subprocess.run([sys.executable, 'manage.py', 'check'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Django local окружение загружается без ошибок")
        else:
            print(f"❌ Ошибка Django: {result.stderr}")
            all_good = False
    except Exception as e:
        print(f"❌ Ошибка тестирования Django: {e}")
        all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ВСЁ ОТЛИЧНО! Архитектура стабилизирована!")
        print("\n🎯 Следующие шаги:")
        print("1. Настроить staging сервер")
        print("2. Протестировать процесс деплоя") 
        print("3. Приступить к OAuth интеграции")
    else:
        print("⚠️ Есть проблемы, нужно исправить")
    
    return all_good

if __name__ == "__main__":
    quick_check()
