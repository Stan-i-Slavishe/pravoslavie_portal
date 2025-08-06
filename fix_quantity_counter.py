#!/usr/bin/env python3
"""
Скрипт для исправления горизонтального расположения кнопок в счетчике количества
"""

import os
import subprocess
import sys

def fix_quantity_counter():
    """Исправление счетчика количества"""
    print("🔧 Исправление горизонтального расположения кнопок...")
    
    # Проверяем наличие CSS файла
    css_file = os.path.join('static', 'css', 'cart_quantity.css')
    if os.path.exists(css_file):
        print("✅ CSS файл cart_quantity.css найден")
    else:
        print("❌ CSS файл cart_quantity.css не найден")
        return False
    
    # Собираем статические файлы
    print("📦 Сбор статических файлов...")
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Статические файлы собраны")
        else:
            print(f"⚠️ Предупреждение при сборе: {result.stderr}")
    except Exception as e:
        print(f"❌ Ошибка при сборе статических файлов: {e}")
    
    print("\n🎯 Рекомендации для исправления:")
    print("1. Убедитесь, что сервер перезапущен: python manage.py runserver")
    print("2. Очистите кеш браузера (Ctrl+F5 или Cmd+Shift+R)")
    print("3. Проверьте, что CSS файл загружается в браузере")
    print("4. Откройте тестовый файл: test_horizontal_quantity_counter.html")
    
    # Проверяем настройки статических файлов в settings.py
    print("\n🔍 Проверка настроек...")
    settings_file = os.path.join('config', 'settings.py')
    if os.path.exists(settings_file):
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'STATICFILES_DIRS' in content:
                print("✅ STATICFILES_DIRS найден в settings.py")
            else:
                print("⚠️ STATICFILES_DIRS не найден в settings.py")
    
    return True

def create_debug_template():
    """Создать отладочный шаблон для проверки"""
    debug_template = """{% extends 'base.html' %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/cart_quantity.css' %}">
<style>
/* Дополнительные стили для отладки */
.debug-box {
    border: 2px solid red;
    background: yellow;
    padding: 10px;
    margin: 10px 0;
}

.quantity-control .input-group {
    border: 2px solid blue !important;
}

.quantity-control .btn {
    border: 2px solid green !important;
}
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>🐛 Отладка счетчика количества</h1>
    
    <div class="debug-box">
        <h3>Тест 1: Базовый счетчик</h3>
        <div class="quantity-control">
            <label class="form-label text-muted small mb-1">Количество:</label>
            <div class="input-group input-group-sm">
                <button type="button" class="btn btn-outline-secondary decrease-btn">
                    <i class="bi bi-dash"></i>
                </button>
                <input type="text" class="form-control text-center quantity-input" value="1" readonly>
                <button type="button" class="btn btn-outline-secondary increase-btn">
                    <i class="bi bi-plus"></i>
                </button>
            </div>
        </div>
    </div>
    
    <div class="debug-box">
        <h3>Тест 2: В карточке товара</h3>
        <div class="card">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-md-4">
                        <h5>Тестовый товар</h5>
                    </div>
                    <div class="col-md-3">
                        <div class="quantity-control">
                            <label class="form-label text-muted small mb-1">Количество:</label>
                            <div class="input-group input-group-sm">
                                <button type="button" class="btn btn-outline-secondary decrease-btn">
                                    <i class="bi bi-dash"></i>
                                </button>
                                <input type="text" class="form-control text-center quantity-input" value="5" readonly>
                                <button type="button" class="btn btn-outline-secondary increase-btn">
                                    <i class="bi bi-plus"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="h5 text-success">2500₽</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="alert alert-info">
        <h4>🔍 Что проверить:</h4>
        <ul>
            <li>Кнопки - и + должны быть рядом горизонтально</li>
            <li>Поле ввода между ними</li>
            <li>Все элементы на одной линии</li>
            <li>CSS файл загружается (проверьте в инструментах разработчика)</li>
        </ul>
    </div>
</div>
{% endblock %}"""
    
    debug_file = os.path.join('templates', 'shop', 'debug_cart.html')
    os.makedirs(os.path.dirname(debug_file), exist_ok=True)
    
    with open(debug_file, 'w', encoding='utf-8') as f:
        f.write(debug_template)
    
    print(f"✅ Создан отладочный шаблон: {debug_file}")
    return debug_file

def add_debug_url():
    """Добавить URL для отладки"""
    urls_file = os.path.join('shop', 'urls.py')
    if os.path.exists(urls_file):
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'debug-cart' not in content:
            # Добавляем URL для отладки
            debug_url = "    path('debug-cart/', views.debug_cart_view, name='debug_cart'),"
            
            # Находим место для вставки (перед последней скобкой)
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() == ']':
                    lines.insert(i, debug_url)
                    break
            
            with open(urls_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            print("✅ Добавлен URL для отладки: /shop/debug-cart/")
        else:
            print("✅ URL для отладки уже существует")

def add_debug_view():
    """Добавить view для отладки"""
    views_file = os.path.join('shop', 'views.py')
    if os.path.exists(views_file):
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'debug_cart_view' not in content:
            debug_view = '''
def debug_cart_view(request):
    """Отладочная страница для счетчика количества"""
    return render(request, 'shop/debug_cart.html')
'''
            
            # Добавляем в конец файла
            with open(views_file, 'a', encoding='utf-8') as f:
                f.write(debug_view)
            
            print("✅ Добавлен view для отладки")
        else:
            print("✅ View для отладки уже существует")

if __name__ == "__main__":
    print("🛠️ ИСПРАВЛЕНИЕ СЧЕТЧИКА КОЛИЧЕСТВА")
    print("=" * 50)
    
    try:
        # Основные исправления
        if fix_quantity_counter():
            # Создаем отладочные инструменты
            create_debug_template()
            add_debug_url()
            add_debug_view()
            
            print("\n" + "=" * 50)
            print("✅ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!")
            print("\n🚀 Следующие шаги:")
            print("1. Перезапустите сервер: python manage.py runserver")
            print("2. Очистите кеш браузера (Ctrl+F5)")
            print("3. Откройте корзину: http://127.0.0.1:8000/shop/cart/")
            print("4. Для отладки: http://127.0.0.1:8000/shop/debug-cart/")
            
            print("\n🔧 Если проблема не решена:")
            print("- Проверьте консоль браузера на ошибки CSS")
            print("- Убедитесь, что файл cart_quantity.css загружается")
            print("- Проверьте настройки STATICFILES_DIRS в settings.py")
            
        else:
            print("❌ Не удалось применить исправления")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
