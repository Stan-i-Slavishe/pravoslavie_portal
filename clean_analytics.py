#!/usr/bin/env python
"""
Очистка всех файлов аналитики и пересборка статики
"""
import os
import shutil
from pathlib import Path

def clean_analytics_files():
    base_dir = Path('E:/pravoslavie_portal')
    
    print("🧹 Очистка файлов аналитики...")
    
    # Папки для очистки
    staticfiles_js = base_dir / 'staticfiles' / 'js'
    static_js = base_dir / 'static' / 'js'
    
    # Файлы аналитики для удаления
    analytics_files = [
        'analytics.js',
        'analytics.js.gz', 
        'purchase_intent_tracker.js',
        'purchase_intent_tracker.js.gz'
    ]
    
    # Паттерны файлов с хешами
    analytics_patterns = [
        'analytics.',
        'purchase_intent_tracker.'
    ]
    
    # Удаляем из staticfiles
    if staticfiles_js.exists():
        for file in staticfiles_js.glob('*'):
            if any(pattern in file.name for pattern in analytics_patterns):
                try:
                    file.unlink()
                    print(f"🗑️ Удален: {file}")
                except Exception as e:
                    print(f"❌ Ошибка удаления {file}: {e}")
    
    # Удаляем из static если есть нежелательные файлы
    if static_js.exists():
        for filename in analytics_files:
            file_path = static_js / filename
            if file_path.exists() and filename != 'analytics.js':  # Оставляем нашу заглушку
                try:
                    file_path.unlink()
                    print(f"🗑️ Удален: {file_path}")
                except Exception as e:
                    print(f"❌ Ошибка удаления {file_path}: {e}")
    
    print("✅ Очистка завершена!")

if __name__ == '__main__':
    clean_analytics_files()
