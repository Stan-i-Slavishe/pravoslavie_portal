#!/usr/bin/env python
"""
Полная настройка HTTPS для Django - один скрипт
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Выполняет команду и показывает результат"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - готово")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка: {e}")
        if e.stdout:
            print(f"Вывод: {e.stdout}")
        if e.stderr:
            print(f"Ошибка: {e.stderr}")
        return False

def main():
    print("🔧 НАСТРОЙКА DJANGO ДЛЯ HTTPS")
    print("=" * 40)
    
    if not os.path.exists('manage.py'):
        print("❌ Запустите скрипт из корня Django проекта")
        return
    
    print("\n1️⃣ Настраиваем Django settings...")
    exec(open('add_https_support.py').read())
    
    print("\n2️⃣ Устанавливаем django-extensions...")
    if run_command("pip install django-extensions werkzeug", "Установка django-extensions"):
        print("✅ django-extensions установлен")
    
    print("\n3️⃣ Создаем SSL сертификат...")
    exec(open('create_ssl.py').read())
    
    print("\n🎉 НАСТРОЙКА ЗАВЕРШЕНА!")
    print("=" * 40)
    
    print("\n📋 ВАРИАНТЫ ЗАПУСКА:")
    print("🌐 HTTP сервер:")
    print("   python manage.py runserver")
    print("   Адрес: http://127.0.0.1:8000/")
    print()
    print("🔒 HTTPS сервер:")
    print("   python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem")
    print("   Адрес: https://127.0.0.1:8000/")
    print("   ⚠️ Браузер покажет предупреждение - нажмите 'Дополнительно' -> 'Перейти на сайт'")
    
    choice = input("\nЗапустить сервер сейчас? (1=HTTP, 2=HTTPS, n=Нет): ")
    
    if choice == "1":
        print("\n🌐 Запускаем HTTP сервер...")
        os.system("python manage.py runserver")
    elif choice == "2":
        print("\n🔒 Запускаем HTTPS сервер...")
        if os.path.exists('ssl/cert.pem'):
            os.system("python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem")
        else:
            print("❌ SSL сертификат не найден. Сначала создайте его.")
    else:
        print("\n✅ Готово! Используйте команды выше для запуска.")

if __name__ == '__main__':
    main()
