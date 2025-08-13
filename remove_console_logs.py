#!/usr/bin/env python3
"""
Скрипт для удаления console.log из production версии
"""

def remove_console_logs():
    """Удаляет console.log из шаблона для продакшена"""
    
    template_path = "E:/pravoslavie_portal/templates/core/categories.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Убираем все строки с console.log
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            if 'console.log(' not in line:
                cleaned_lines.append(line)
            else:
                print(f"Удалена строка: {line.strip()}")
        
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Сохраняем очищенную версию
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print("✅ Console.log удалены из production версии")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🧹 Очистка console.log для продакшена...")
    remove_console_logs()
