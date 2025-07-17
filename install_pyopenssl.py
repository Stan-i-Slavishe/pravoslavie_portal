#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Доустановка pyOpenSSL и запуск HTTPS
"""
import subprocess
import sys
import os

def install_pyopenssl():
    """Устанавливает pyOpenSSL"""
    print("📦 Устанавливаем pyOpenSSL...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyOpenSSL'], 
                      check=True, capture_output=True)
        print("✅ pyOpenSSL установлен")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки: {e}")
        return False

def main():
    print("🔧 ДОУСТАНОВКА pyOpenSSL ДЛЯ HTTPS")
    print("=" * 40)
    
    if not install_pyopenssl():
        print("❌ Не удалось установить pyOpenSSL")
        return
    
    print("\n✅ Все готово для HTTPS!")
    print("\n📋 ЗАПУСК СЕРВЕРОВ:")
    print("🌐 HTTP:  start_http.bat  или  python manage.py runserver")
    print("🔒 HTTPS: start_https.bat или  python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem")
    
    choice = input("\nЗапустить HTTPS сервер сейчас? (y/n): ")
    
    if choice.lower() == 'y':
        print("\n🔒 Запускаем HTTPS сервер...")
        print("   Адрес: https://127.0.0.1:8000/")
        print("   ⚠️ Браузер покажет предупреждение - нажмите 'Дополнительно' -> 'Перейти на сайт'")
        print()
        os.system("python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem")
    else:
        print("\n✅ Готово! Используйте start_https.bat когда будете готовы")

if __name__ == '__main__':
    main()
