#!/usr/bin/env python
"""
Скрипт для удаления заглушек аналитики и очистки системы

Этот скрипт:
1. Переименовывает analytics.js для предотвращения случайного подключения
2. Создает резервную копию
3. Очищает статические файлы аналитики
"""

import os
import shutil
from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    
    print("🧹 Очистка заглушек аналитики...")
    
    # 1. Переименовываем analytics.js
    analytics_js = base_dir / 'static' / 'js' / 'analytics.js'
    if analytics_js.exists():
        backup_name = base_dir / 'static' / 'js' / 'analytics.js.disabled'
        shutil.move(str(analytics_js), str(backup_name))
        print(f"✅ Переименовал {analytics_js} → {backup_name}")
    
    # 2. Очищаем staticfiles с аналитикой
    staticfiles_dir = base_dir / 'staticfiles' / 'js'
    if staticfiles_dir.exists():
        for file in staticfiles_dir.glob('analytics.*'):
            file.unlink()
            print(f"🗑️ Удален {file}")
    
    # 3. Создаем заглушку для analytics.js (на случай если что-то еще пытается его подключить)
    stub_content = """// analytics.js - ОТКЛЮЧЕН
// Система аналитики отключена. Заглушки удалены.
console.log('📊 Аналитика покупательских намерений отключена');

// Пустые функции для обратной совместимости
window.analytics = {
    trackPurchaseIntent: () => {},
    showSubscriptionModal: () => {},
    disabled: true
};
"""
    
    with open(analytics_js, 'w', encoding='utf-8') as f:
        f.write(stub_content)
    
    print(f"✅ Создана заглушка {analytics_js}")
    
    print("\n🎉 Очистка завершена!")
    print("\n📋 Что было сделано:")
    print("   • Отключена аналитика в config/urls.py")
    print("   • Отключена аналитика в config/settings.py") 
    print("   • Убраны заглушки из templates/fairy_tales/fairy_tale_detail.html")
    print("   • Добавлен URL для скачивания бесплатных сказок")
    print("   • Добавлена функция download_free_tale в fairy_tales/views.py")
    print("   • Очищены статические файлы аналитики")
    print("\n🚀 Система готова к продакшену без заглушек!")

if __name__ == '__main__':
    main()
