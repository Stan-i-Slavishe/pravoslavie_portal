#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка и восстановление повреждённых файлов
"""

import os
import glob

def check_python_file(filepath):
    """Проверяет Python файл на синтаксические ошибки"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем базовые проблемы
        if not content.strip():
            return f"❌ ПУСТОЙ: {filepath}"
        
        if content.startswith('from django.db ') and len(content) < 50:
            return f"❌ ОБРЕЗАН: {filepath}"
        
        if content.startswith('from django.contrib ') and len(content) < 50:
            return f"❌ ОБРЕЗАН: {filepath}"
            
        if content.startswith('return f"') and not content.startswith('def '):
            return f"❌ ПОВРЕЖДЁН: {filepath}"
            
        # Проверяем компиляцию
        try:
            compile(content, filepath, 'exec')
            return f"✅ OK: {filepath}"
        except SyntaxError as e:
            return f"❌ СИНТАКСИС: {filepath} - {e}"
            
    except Exception as e:
        return f"❌ ОШИБКА: {filepath} - {e}"

def main():
    print("🔍 ПРОВЕРКА ФАЙЛОВ DJANGO")
    print("=" * 50)
    
    # Проверяем основные Python файлы Django
    patterns = [
        '*/models.py',
        '*/admin.py', 
        '*/views.py',
        '*/forms.py',
        '*/urls.py',
    ]
    
    damaged_files = []
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        for file in files:
            if '.venv' not in file and '__pycache__' not in file:
                result = check_python_file(file)
                print(result)
                if result.startswith('❌'):
                    damaged_files.append(file)
    
    if damaged_files:
        print("\n" + "=" * 50)
        print("🚨 НАЙДЕНЫ ПОВРЕЖДЁННЫЕ ФАЙЛЫ:")
        for file in damaged_files:
            print(f"   📄 {file}")
            
        print(f"\n💡 Нужно восстановить {len(damaged_files)} файлов из резервных копий (.bak)")
        
        # Попробуем автоматически восстановить
        print("\n🔧 ПОПЫТКА АВТОВОССТАНОВЛЕНИЯ...")
        for file in damaged_files:
            backup_file = f"{file}.bak"
            if os.path.exists(backup_file):
                try:
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        backup_content = f.read()
                    
                    # Убираем только импорты комментариев
                    lines = backup_content.split('\n')
                    clean_lines = []
                    
                    for line in lines:
                        if any(comment_word in line.lower() for comment_word in ['comment_admin', 'from .comment_admin', 'comments = GenericRelation']):
                            continue
                        clean_lines.append(line)
                    
                    clean_content = '\n'.join(clean_lines)
                    
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(clean_content)
                    
                    print(f"✅ Восстановлен: {file}")
                except Exception as e:
                    print(f"❌ Не удалось восстановить {file}: {e}")
            else:
                print(f"⚠️ Нет резервной копии для {file}")
    else:
        print("\n✅ ВСЕ ФАЙЛЫ В ПОРЯДКЕ!")

if __name__ == "__main__":
    main()
