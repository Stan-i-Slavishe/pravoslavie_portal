#!/usr/bin/env python3
"""
Проверка шаблонов на синтаксические ошибки
"""
import os
import re

def check_template_syntax(file_path):
    """Проверяет синтаксис Django шаблона"""
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
        # Проверяем парность блоков
        block_stack = []
        for i, line in enumerate(lines, 1):
            # Ищем открывающие блоки
            block_matches = re.findall(r'{%\s*block\s+(\w+)', line)
            for block_name in block_matches:
                block_stack.append((block_name, i))
            
            # Ищем закрывающие блоки
            endblock_matches = re.findall(r'{%\s*endblock\s*(\w+)?', line)
            for endblock_match in endblock_matches:
                if not block_stack:
                    errors.append(f"Строка {i}: endblock без соответствующего block")
                else:
                    block_name, block_line = block_stack.pop()
                    if endblock_match and endblock_match != block_name:
                        errors.append(f"Строка {i}: endblock {endblock_match} не соответствует block {block_name} (строка {block_line})")
        
        # Проверяем незакрытые блоки
        for block_name, block_line in block_stack:
            errors.append(f"Строка {block_line}: block {block_name} не закрыт")
            
    except Exception as e:
        errors.append(f"Ошибка чтения файла: {e}")
    
    return errors

def scan_templates():
    """Сканирует все шаблоны в проекте"""
    template_dirs = [
        'templates',
        'stories/templates',
        'books/templates', 
        'fairy_tales/templates',
        'shop/templates',
        'accounts/templates',
        'core/templates'
    ]
    
    print("🔍 Проверка синтаксиса Django шаблонов...")
    print("=" * 50)
    
    all_good = True
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        errors = check_template_syntax(file_path)
                        
                        if errors:
                            all_good = False
                            print(f"❌ {file_path}:")
                            for error in errors:
                                print(f"   {error}")
                            print()
                        else:
                            print(f"✅ {file_path}")
    
    if all_good:
        print("\n🎉 Все шаблоны синтаксически корректны!")
    else:
        print("\n⚠️  Найдены ошибки в шаблонах. Исправьте их перед запуском.")

if __name__ == "__main__":
    scan_templates()
