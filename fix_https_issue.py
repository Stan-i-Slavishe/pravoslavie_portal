#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления HTTPS проблем в Django development сервере
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("🔧 Исправление HTTPS проблем Django development сервера")
    print("=" * 60)
    
    # Переходим в директорию проекта
    project_dir = Path("E:/pravoslavie_portal")
    os.chdir(project_dir)
    
    print("1. 🛑 Останавливаем все процессы Django...")
    try:
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                      capture_output=True, check=False)
    except:
        pass
    
    print("2. 🧹 Очищаем Django кеш...")
    try:
        subprocess.run([
            str(project_dir / ".venv" / "Scripts" / "python.exe"),
            "manage.py", "clearcache"
        ], capture_output=True, check=False)
    except:
        pass
    
    print("3. 🗂️ Очищаем __pycache__ файлы...")
    for pycache in project_dir.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache)
        except:
            pass
    
    print("4. 📁 Очищаем временные файлы...")
    temp_patterns = ["*.pyc", "*.pyo", ".DS_Store", "Thumbs.db"]
    for pattern in temp_patterns:
        for file in project_dir.rglob(pattern):
            try:
                file.unlink()
            except:
                pass
    
    print("\n✅ Система очищена!")
    print("\n📋 СЛЕДУЮЩИЕ ШАГИ:")
    print("   1. Очистите кеш браузера (Ctrl+Shift+Delete)")
    print("   2. Запустите: start_server_fixed.bat")
    print("   3. Используйте ТОЛЬКО: http://127.0.0.1:8000")
    print("   4. НЕ используйте https://")
    
    print("\n🌐 Для автоматического запуска:")
    print("   python fix_https_issue.py --start")
    
    if "--start" in sys.argv:
        print("\n🚀 Запускаем сервер...")
        subprocess.run([
            str(project_dir / "start_server_fixed.bat")
        ], shell=True)

if __name__ == "__main__":
    main()
