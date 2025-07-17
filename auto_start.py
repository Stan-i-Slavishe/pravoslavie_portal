#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматическое исправление проблем с allauth и запуск сервера
"""
import os
import sys
import subprocess
from pathlib import Path

def fix_allauth_issues():
    """Исправляет проблемы с allauth импортами"""
    print("🔧 Исправление проблем с allauth...")
    
    # Проверяем наличие allauth в установленных пакетах
    try:
        import allauth
        print("✅ Allauth установлен")
        return True
    except ImportError:
        print("⚠️  Allauth не установлен")
        return False

def main():
    print("🚀 Автоматическое исправление и запуск Django сервера")
    print("=" * 60)
    
    project_dir = Path("E:/pravoslavie_portal")
    os.chdir(project_dir)
    
    # Проверяем и исправляем проблемы
    allauth_available = fix_allauth_issues()
    
    print("\n📋 Доступные режимы запуска:")
    print("1. Быстрый (без Allauth) - config.settings_quick")
    print("2. С Allauth - config.settings_with_allauth") 
    print("3. Полный (основной) - config.settings")
    
    # Автоматический выбор настроек
    if "--quick" in sys.argv or not allauth_available:
        settings = "config.settings_quick"
        print(f"\n🎯 Выбран быстрый режим: {settings}")
    elif "--allauth" in sys.argv and allauth_available:
        settings = "config.settings_with_allauth"
        print(f"\n🎯 Выбран режим с Allauth: {settings}")
    else:
        settings = "config.settings"
        print(f"\n🎯 Выбран полный режим: {settings}")
    
    # Останавливаем существующие процессы
    print("\n1. 🛑 Останавливаем существующие процессы...")
    try:
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                      capture_output=True, check=False)
    except:
        pass
    
    python_exe = str(project_dir / ".venv" / "Scripts" / "python.exe")
    
    # Применяем миграции
    print("2. 🗄️  Применяем миграции...")
    try:
        subprocess.run([
            python_exe, "manage.py", "migrate", f"--settings={settings}"
        ], check=True, cwd=project_dir)
        print("   ✅ Миграции применены")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Ошибка миграций: {e}")
        return
    
    # Собираем статические файлы
    print("3. 📊 Собираем статические файлы...")
    try:
        subprocess.run([
            python_exe, "manage.py", "collectstatic", 
            "--noinput", "--clear", f"--settings={settings}"
        ], check=True, cwd=project_dir)
        print("   ✅ Статические файлы собраны")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Ошибка сбора статики: {e}")
    
    print("\n🌐 Запускаем сервер...")
    print("=" * 60)
    print(f"📡 Адрес: http://127.0.0.1:8000")
    print(f"⚙️  Настройки: {settings}")
    print(f"🛑 Остановка: Ctrl+C")
    print("=" * 60)
    
    # Запускаем сервер
    try:
        subprocess.run([
            python_exe, "manage.py", "runserver", "127.0.0.1:8000",
            f"--settings={settings}"
        ], cwd=project_dir)
    except KeyboardInterrupt:
        print("\n\n👋 Сервер остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка запуска сервера: {e}")

if __name__ == "__main__":
    main()
