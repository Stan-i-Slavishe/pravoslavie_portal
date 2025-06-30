#!/usr/bin/env python
"""
Быстрый запуск системы магазина
"""
import subprocess
import sys

def run_command(command, description):
    """Выполнить команду с описанием"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd='E:\\pravoslavie_portal')
        if result.returncode == 0:
            print(f"✅ {description} - Готово!")
            return True
        else:
            print(f"❌ Ошибка в {description}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Исключение в {description}: {e}")
        return False

def main():
    print("🚀 Быстрая настройка магазина...")
    
    commands = [
        ("python reset_books.py", "Пересоздание книг с правильными slug'ами"),
        ("python init_shop.py", "Инициализация системы магазина"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n❌ Остановлено на этапе: {description}")
            sys.exit(1)
    
    print("\n🎉 Магазин готов к работе!")
    print("\n📋 Что доступно:")
    print("1. 🛒 Каталог товаров: http://127.0.0.1:8000/shop/")
    print("2. 📚 Библиотека: http://127.0.0.1:8000/books/")
    print("3. 🎛️ Админ-панель: http://127.0.0.1:8000/admin/")
    print("\n🔧 Функциональность:")
    print("• ✅ Добавление товаров в корзину")
    print("• ✅ Оформление заказов")
    print("• ✅ Тестовая система оплаты")
    print("• ✅ Скачивание купленных книг")
    print("• ✅ Система промокодов")
    print("• ✅ Личный кабинет покупок")
    
    print(f"\n🎯 Тестовые промокоды:")
    print("• WELCOME10 - скидка 10%")
    print("• BOOK50 - скидка 50₽") 
    print("• PRAVOSLAVIE - скидка 15%")

if __name__ == '__main__':
    main()
