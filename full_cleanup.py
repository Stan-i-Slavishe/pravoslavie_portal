#!/usr/bin/env python
"""
Полная очистка кеша и статических файлов для удаления заглушек
"""
import os
import shutil
from pathlib import Path

def full_cleanup():
    base_dir = Path('E:/pravoslavie_portal')
    
    print("🧹 Полная очистка заглушек...")
    
    # 1. Удаляем всю папку staticfiles
    staticfiles_dir = base_dir / 'staticfiles'
    if staticfiles_dir.exists():
        print(f"🗑️ Удаляем {staticfiles_dir}")
        shutil.rmtree(staticfiles_dir)
    
    # 2. Пересоздаем staticfiles
    staticfiles_dir.mkdir()
    (staticfiles_dir / 'js').mkdir()
    (staticfiles_dir / 'css').mkdir()
    
    print("✅ Staticfiles очищены")
    
    # 3. Создаем блокирующий файл в staticfiles
    blocker_content = """
// БЛОКИРОВЩИК ЗАГЛУШЕК - НЕ УДАЛЯТЬ!
console.log('🚫 Все заглушки заблокированы');
window.showComingSoonModal = () => false;
window.trackPurchaseIntent = () => false;
"""
    
    with open(staticfiles_dir / 'js' / 'purchase_intent_tracker.js', 'w') as f:
        f.write(blocker_content)
    
    with open(staticfiles_dir / 'js' / 'analytics.js', 'w') as f:
        f.write(blocker_content)
    
    print("✅ Блокирующие файлы созданы")
    
    # 4. Проверяем static/js
    static_js = base_dir / 'static' / 'js'
    problem_files = [
        'purchase_intent_tracker.js',
        'analytics.js'
    ]
    
    for filename in problem_files:
        file_path = static_js / filename
        if file_path.exists():
            with open(file_path, 'w') as f:
                f.write(blocker_content)
            print(f"✅ Заблокирован {filename}")
    
    print("\n🎉 Полная очистка завершена!")
    print("Перезапустите сервер Django и обновите страницу с Ctrl+F5")

if __name__ == '__main__':
    full_cleanup()
