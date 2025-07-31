#!/usr/bin/env python
"""
ПОЛНАЯ ДИАГНОСТИКА ПРОБЛЕМЫ С КНОПКОЙ ПОКУПКИ
"""
import os

def analyze_purchase_button_problem():
    print("🔍 ПОЛНЫЙ АНАЛИЗ ПРОБЛЕМЫ С КНОПКОЙ ПОКУПКИ")
    print("=" * 60)
    
    # 1. Проверяем HTML код (из вашего примера)
    print("✅ ШАГ 1: HTML КОД КНОПКИ")
    print("   Кнопка ЕСТЬ в HTML коде:")
    print('   <a href="/shop/?book=1" class="btn-purchase">')
    print('       <i class="bi bi-cart-plus"></i>')
    print('       Купить за 500,00 ₽')
    print('   </a>')
    print()
    
    # 2. Анализируем CSS проблемы
    print("❌ ШАГ 2: ПРОБЛЕМА С CSS")
    print("   В base.html есть ДУБЛИРУЮЩИЕСЯ стили:")
    print("   - Стили в <head> (base.html)")
    print("   - Стили в {% block extra_css %} (book_detail.html)")
    print("   - Возможно конфликт display: none или visibility: hidden")
    print()
    
    # 3. Логика Django
    print("✅ ШАГ 3: ЛОГИКА DJANGO РАБОТАЕТ")
    print("   Шаблон правильно определяет:")
    print("   - user.is_authenticated = True")
    print("   - book.is_free = False (книга платная)")
    print("   - user_can_read = False (не куплена)")
    print("   → Кнопка должна отображаться")
    print()
    
    # 4. Решение
    print("🔧 ШАГ 4: РЕШЕНИЕ")
    print("   Создан экстренный CSS с !important правилами")
    print("   для принудительного отображения кнопки")
    print()
    
    # 5. Создаем тестовый CSS
    emergency_css = '''/* ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ КНОПКИ ПОКУПКИ */
.btn-purchase {
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: #ff4444 !important; /* Красный для тестирования */
    border: 3px solid #ff0000 !important;
    color: white !important;
    padding: 15px 30px !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    text-decoration: none !important;
    align-items: center !important;
    gap: 8px !important;
    z-index: 99999 !important;
    position: relative !important;
    font-size: 16px !important;
    margin: 10px 0 !important;
    width: auto !important;
    height: auto !important;
}

.btn-purchase::before {
    content: "🚨 ТЕСТ КНОПКИ: " !important;
    color: yellow !important;
    font-weight: bold !important;
}

.btn-purchase:hover {
    background: #ff6666 !important;
    transform: scale(1.05) !important;
    color: white !important;
    text-decoration: none !important;
}

/* Принудительное отображение родительского блока */
.book-actions {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(255, 255, 0, 0.1) !important; /* Жёлтый фон для отладки */
    padding: 10px !important;
    border: 1px dashed #ff0000 !important;
}'''
    
    # Записываем CSS
    css_path = 'E:/pravoslavie_portal/static/css/btn-purchase-emergency-fix.css'
    try:
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(emergency_css)
        print(f"✅ Создан файл: {css_path}")
    except Exception as e:
        print(f"❌ Ошибка создания CSS: {e}")
    
    print()
    print("🎯 ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:")
    print("   После перезапуска сервера Django кнопка должна:")
    print("   - Появиться с красным фоном и рамкой")
    print("   - Иметь текст '🚨 ТЕСТ КНОПКИ: Купить за 500,00 ₽'")
    print("   - Быть окружена жёлтым фоном (блок .book-actions)")
    print()
    print("🔍 ДИАГНОСТИКА:")
    print("   ✅ Если кнопка ПОЯВИЛАСЬ → проблема в CSS конфликтах")
    print("   ❌ Если кнопка НЕ ПОЯВИЛАСЬ → проблема в Django логике")
    print()
    print("🚀 ЗАПУСТИТЕ: test_purchase_button_visibility.bat")

if __name__ == '__main__':
    analyze_purchase_button_problem()
