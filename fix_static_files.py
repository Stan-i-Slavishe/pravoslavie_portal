#!/usr/bin/env python
"""
Скрипт для исправления статических файлов
"""
import os
import sys
import shutil
import subprocess

def main():
    print("🛠️ Исправление статических файлов для кнопки покупки...")
    print()
    
    # Путь к проекту
    project_path = r"E:\pravoslavie_portal"
    os.chdir(project_path)
    
    # Удаляем папку staticfiles
    staticfiles_path = os.path.join(project_path, "staticfiles")
    if os.path.exists(staticfiles_path):
        print("🗑️ Удаляем старые собранные статические файлы...")
        shutil.rmtree(staticfiles_path)
        print("✅ Папка staticfiles удалена")
    else:
        print("⚠️ Папка staticfiles не найдена")
    
    print()
    print("🔄 Пересобираем статические файлы...")
    
    # Выполняем collectstatic
    try:
        result = subprocess.run([
            sys.executable, "manage.py", "collectstatic", "--noinput", "--clear"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Статические файлы успешно собраны")
        else:
            print("❌ Ошибка при сборке статических файлов:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print()
    print("🎯 Проверяем наличие правильного CSS файла...")
    
    purchase_button_css = os.path.join(staticfiles_path, "css", "purchase-button-fix.css")
    if os.path.exists(purchase_button_css):
        print("✅ purchase-button-fix.css найден")
    else:
        print("❌ purchase-button-fix.css НЕ найден!")
    
    print()
    print("📝 СЛЕДУЮЩИЕ ШАГИ:")
    print("1. Перезапустите Django сервер")
    print("2. Очистите кеш браузера (Ctrl+F5)")
    print("3. Проверьте страницу книги")
    print()
    print("✨ Готово!")

if __name__ == "__main__":
    main()
