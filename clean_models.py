#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧹 ОЧИСТКА MODELS.PY ОТ КОММЕНТАРИЕВ
Удаляет все модели комментариев из stories/models.py
"""

import re

def clean_models_file():
    print("🧹 ОЧИСТКА stories/models.py ОТ МОДЕЛЕЙ КОММЕНТАРИЕВ")
    print("=" * 55)
    
    models_file = 'stories/models.py'
    
    try:
        # Читаем файл
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 Читаем файл: {models_file}")
        
        # Удаляем модели комментариев
        models_to_remove = [
            'StoryComment',
            'StoryCommentLike', 
            'CommentReport'
        ]
        
        for model_name in models_to_remove:
            # Паттерн для поиска класса модели
            pattern = rf'class {model_name}\([^)]*\):.*?(?=\n\nclass|\n\n\S|\Z)'
            
            # Удаляем модель
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            print(f"✅ Удалена модель: {model_name}")
        
        # Очищаем пустые строки
        content = re.sub(r'\n\n\n+', '\n\n', content)
        content = content.strip() + '\n'
        
        # Создаем бэкап
        with open(f'{models_file}.backup', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Записываем очищенный файл
        with open(models_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Файл {models_file} очищен от моделей комментариев")
        print(f"📁 Бэкап сохранен: {models_file}.backup")
        
    except FileNotFoundError:
        print(f"❌ Файл {models_file} не найден")
    except Exception as e:
        print(f"💥 Ошибка: {e}")

if __name__ == "__main__":
    clean_models_file()
