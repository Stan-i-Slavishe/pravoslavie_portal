import os
import subprocess
import sys

def collect_static_files():
    """Собрать статические файлы"""
    print("🔧 Сбор статических файлов...")
    
    try:
        # Запускаем collectstatic
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput'
        ], cwd=os.getcwd(), capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Статические файлы собраны успешно")
            return True
        else:
            print(f"❌ Ошибка при сборе статических файлов: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    collect_static_files()
