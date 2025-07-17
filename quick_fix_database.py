#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрое исправление ошибки KeyError: 'OPTIONS'
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🔧 Исправление ошибки KeyError: 'OPTIONS'")
    print("=" * 50)
    
    project_dir = Path("E:/pravoslavie_portal")
    os.chdir(project_dir)
    
    print("1. ✅ Исправлена ошибка в config/settings.py")
    print("2. ✅ Создан config/settings_quick.py для быстрого запуска")
    print("3. ✅ Создан start_quick.bat для безопасного запуска")
    
    print("\n🚀 Варианты запуска:")
    print("   A) Быстрый запуск: start_quick.bat")
    print("   B) Обычный запуск: python manage.py runserver")
    print("   C) Автоматический запуск: python quick_fix_database.py --start")
    
    if "--start" in sys.argv:
        print("\n🌐 Запускаем быстрый сервер...")
        try:
            subprocess.run([
                str(project_dir / ".venv" / "Scripts" / "python.exe"),
                "manage.py", "runserver", "127.0.0.1:8000",
                "--settings=config.settings_quick"
            ], cwd=project_dir)
        except KeyboardInterrupt:
            print("\n👋 Сервер остановлен")
    
    print("\n✅ Проблема решена!")
    print("🌐 Используйте: http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
