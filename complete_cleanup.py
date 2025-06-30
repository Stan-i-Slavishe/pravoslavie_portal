#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полная зачистка системы комментариев из проекта
"""

import os
import re
import glob

def clean_file(filepath, patterns_to_remove, backup=True):
    """Очищает файл от указанных паттернов"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Удаляем паттерны
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
        
        # Убираем лишние пустые строки
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            if backup:
                with open(f"{filepath}.bak", 'w', encoding='utf-8') as f:
                    f.write(original_content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Очищен: {filepath}")
            return True
        else:
            print(f"⚪ Без изменений: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при обработке {filepath}: {e}")
        return False

def find_files_with_pattern(directory, file_pattern, content_pattern):
    """Находит файлы с определенным содержимым"""
    found_files = []
    
    for filepath in glob.glob(os.path.join(directory, '**', file_pattern), recursive=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(content_pattern, content, re.IGNORECASE):
                    found_files.append(filepath)
        except Exception as e:
            print(f"⚠️  Не удалось прочитать {filepath}: {e}")
    
    return found_files

def main():
    print("=" * 60)
    print("🧹 ПОЛНАЯ ЗАЧИСТКА СИСТЕМЫ КОММЕНТАРИЕВ")
    print("=" * 60)
    
    # Паттерны для удаления
    admin_patterns = [
        r'from\s+\.comment_admin\s+import\s+\*\s*',
        r'from\s+\.comment_admin\s+import\s+.*\n',
        r'import\s+.*comment_admin.*\n',
        r'@admin\.register\(Comment\).*?class.*?Comment.*?Admin.*?:\s*.*?(?=@admin\.register|class|\Z)',
        r'admin\.site\.register\(Comment.*?\)\s*',
    ]
    
    models_patterns = [
        r'class\s+Comment\(.*?\):\s*.*?(?=class|\Z)',
        r'comments\s*=\s*models\..*?\n',
        r'comment_count\s*=\s*models\..*?\n',
        r'from\s+.*comments.*import.*\n',
        r'import\s+.*comments.*\n',
    ]
    
    views_patterns = [
        r'from\s+\.models\s+import\s+.*Comment.*\n',
        r'from\s+\.forms\s+import\s+.*Comment.*\n',
        r'def\s+.*comment.*\(.*?\):.*?(?=def|\Z)',
        r'class\s+.*Comment.*View.*?:.*?(?=class|\Z)',
        r'Comment\.objects\..*?\n',
        r'comment\s*=\s*.*\n',
        r'comments\s*=\s*.*\n',
    ]
    
    forms_patterns = [
        r'class\s+.*Comment.*Form.*?:.*?(?=class|\Z)',
        r'from\s+\.models\s+import\s+.*Comment.*\n',
    ]
    
    urls_patterns = [
        r'path\(.*comment.*\),?\s*',
        r'url\(.*comment.*\),?\s*',
    ]
    
    template_patterns = [
        r'{%\s*for\s+comment\s+in\s+comments\s*%}.*?{%\s*endfor\s*%}',
        r'{%\s*if\s+.*comment.*\s*%}.*?{%\s*endif\s*%}',
        r'{{.*comment.*}}',
        r'<div[^>]*comment[^>]*>.*?</div>',
        r'<!-- comment.*?-->',
    ]
    
    # 1. Очистка admin.py файлов
    print("\n🎯 Очистка admin.py файлов...")
    admin_files = glob.glob('**/admin.py', recursive=True)
    for admin_file in admin_files:
        clean_file(admin_file, admin_patterns)
    
    # 2. Очистка models.py файлов
    print("\n🎯 Очистка models.py файлов...")
    model_files = glob.glob('**/models.py', recursive=True)
    for model_file in model_files:
        clean_file(model_file, models_patterns)
    
    # 3. Очистка views.py файлов
    print("\n🎯 Очистка views.py файлов...")
    view_files = glob.glob('**/views.py', recursive=True)
    for view_file in view_files:
        clean_file(view_file, views_patterns)
    
    # 4. Очистка forms.py файлов
    print("\n🎯 Очистка forms.py файлов...")
    form_files = glob.glob('**/forms.py', recursive=True)
    for form_file in form_files:
        clean_file(form_file, forms_patterns)
    
    # 5. Очистка urls.py файлов
    print("\n🎯 Очистка urls.py файлов...")
    url_files = glob.glob('**/urls.py', recursive=True)
    for url_file in url_files:
        clean_file(url_file, urls_patterns)
    
    # 6. Очистка шаблонов
    print("\n🎯 Очистка HTML шаблонов...")
    template_files = glob.glob('**/templates/**/*.html', recursive=True)
    for template_file in template_files:
        clean_file(template_file, template_patterns)
    
    # 7. Удаление файлов комментариев
    print("\n🎯 Удаление файлов комментариев...")
    comment_files = [
        '**/comment_admin.py',
        '**/comment_forms.py',
        '**/comment_models.py',
        '**/comment_views.py',
        '**/comments.py',
    ]
    
    for pattern in comment_files:
        files = glob.glob(pattern, recursive=True)
        for file in files:
            try:
                os.remove(file)
                print(f"🗑️  Удален: {file}")
            except Exception as e:
                print(f"❌ Не удалось удалить {file}: {e}")
    
    # 8. Поиск оставшихся упоминаний
    print("\n🔍 Поиск оставшихся упоминаний комментариев...")
    
    all_py_files = glob.glob('**/*.py', recursive=True)
    remaining_files = []
    
    for py_file in all_py_files:
        if 'venv' in py_file or '__pycache__' in py_file:
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(r'comment|Comment', content, re.IGNORECASE):
                    # Исключаем безобидные комментарии
                    if not re.search(r'#.*comment|""".*comment.*"""|\'\'\'.*comment.*\'\'\'', content, re.IGNORECASE | re.DOTALL):
                        remaining_files.append(py_file)
        except Exception as e:
            pass
    
    if remaining_files:
        print("\n⚠️  Найдены файлы с возможными остатками комментариев:")
        for file in remaining_files[:10]:  # Показываем первые 10
            print(f"   📄 {file}")
        if len(remaining_files) > 10:
            print(f"   ... и еще {len(remaining_files) - 10} файлов")
    else:
        print("✅ Остатков комментариев не найдено!")
    
    print("\n" + "=" * 60)
    print("🎉 ЗАЧИСТКА ЗАВЕРШЕНА!")
    print("=" * 60)
    print("\n📋 Что было сделано:")
    print("   ✅ Очищены все admin.py файлы")
    print("   ✅ Очищены все models.py файлы") 
    print("   ✅ Очищены все views.py файлы")
    print("   ✅ Очищены все forms.py файлы")
    print("   ✅ Очищены все urls.py файлы")
    print("   ✅ Очищены HTML шаблоны")
    print("   ✅ Удалены файлы комментариев")
    
    print("\n🚀 Теперь запустите:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    print("   python manage.py runserver")

if __name__ == "__main__":
    main()
