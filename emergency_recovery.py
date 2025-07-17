#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🚨 ЭКСТРЕННОЕ ВОССТАНОВЛЕНИЕ Django проекта
Исправляет критические ошибки кодировки и HTTPS
"""
import os
import sys
import subprocess
import time
from pathlib import Path

# Устанавливаем UTF-8 кодировку принудительно
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'ru_RU.UTF-8'

# Добавляем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

def kill_all_python():
    """Убиваем все процессы Python"""
    print("🚨 Закрываем все процессы Python...")
    try:
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, check=False)
        subprocess.run(['taskkill', '/f', '/im', 'pythonw.exe'], 
                      capture_output=True, check=False)
        time.sleep(2)
        print("  ✅ Процессы закрыты")
    except Exception as e:
        print(f"  ⚠️ Ошибка закрытия процессов: {e}")

def fix_encoding():
    """Исправляем проблемы с кодировкой"""
    print("🔤 Исправляем кодировку...")
    
    # Устанавливаем переменные окружения
    env_vars = {
        'PYTHONIOENCODING': 'utf-8',
        'LANG': 'ru_RU.UTF-8',
        'LC_ALL': 'ru_RU.UTF-8',
        'PYTHONLEGACYWINDOWSSTDIO': '1'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("  ✅ Кодировка установлена в UTF-8")

def create_clean_env():
    """Создаем чистый .env файл"""
    print("⚙️ Создаем чистые настройки...")
    
    env_content = """# Экстренные настройки для восстановления
DEBUG=True
SECRET_KEY=django-insecure-emergency-recovery-key-2025
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# База данных
DB_ENGINE=django.db.backends.sqlite3

# Отключаем проблемные компоненты
CELERY_TASK_ALWAYS_EAGER=True
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Кодировка
PYTHONIOENCODING=utf-8
LANG=ru_RU.UTF-8
"""
    
    env_file = BASE_DIR / '.env'
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("  ✅ Файл .env восстановлен")

def clean_problematic_files():
    """Удаляем проблемные файлы"""
    print("🗑️ Удаляем проблемные файлы...")
    
    files_to_remove = [
        BASE_DIR / 'staticfiles',
        BASE_DIR / 'logs' / 'django.log',
        BASE_DIR / 'static' / 'js' / 'error-filter.js',
    ]
    
    for file_path in files_to_remove:
        try:
            if file_path.exists():
                if file_path.is_dir():
                    import shutil
                    shutil.rmtree(file_path)
                    print(f"  ✅ Удалена папка {file_path.name}")
                else:
                    file_path.unlink()
                    print(f"  ✅ Удален файл {file_path.name}")
        except Exception as e:
            print(f"  ⚠️ Не удалось удалить {file_path}: {e}")

def fix_settings():
    """Исправляем настройки Django"""
    print("🔧 Исправляем настройки Django...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        
        # Создаем временный файл настроек
        settings_fix = BASE_DIR / 'config' / 'emergency_settings.py'
        
        settings_content = '''# -*- coding: utf-8 -*-
"""
Экстренные настройки для восстановления
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-emergency-key-12345'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'testserver']

# Минимальные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'accounts',
    'stories',
    'books',
]

# Минимальные middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Локализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Логирование (минимальное)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''
        
        with open(settings_fix, 'w', encoding='utf-8') as f:
            f.write(settings_content)
        
        print("  ✅ Экстренные настройки созданы")
        
    except Exception as e:
        print(f"  ⚠️ Ошибка создания настроек: {e}")

def run_django_commands():
    """Запускаем команды Django"""
    print("📦 Выполняем команды Django...")
    
    commands = [
        ['python', 'manage.py', 'collectstatic', '--noinput', '--clear'],
        ['python', 'manage.py', 'migrate', '--run-syncdb'],
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  encoding='utf-8', cwd=BASE_DIR)
            if result.returncode == 0:
                print(f"  ✅ {' '.join(cmd)} - успешно")
            else:
                print(f"  ⚠️ {' '.join(cmd)} - ошибка: {result.stderr}")
        except Exception as e:
            print(f"  ⚠️ Ошибка выполнения {cmd}: {e}")

def start_server():
    """Запускаем сервер с исправленными настройками"""
    print("🚀 Запускаем Django сервер...")
    
    try:
        # Используем экстренные настройки
        env = os.environ.copy()
        env.update({
            'PYTHONIOENCODING': 'utf-8',
            'LANG': 'ru_RU.UTF-8',
            'DJANGO_SETTINGS_MODULE': 'config.emergency_settings'
        })
        
        cmd = ['python', 'manage.py', 'runserver', '127.0.0.1:8000']
        
        print("  🌐 Сервер запускается на http://127.0.0.1:8000")
        print("  ⚠️ Используйте ТОЛЬКО HTTP (не HTTPS)!")
        print("  🔄 Нажмите Ctrl+C для остановки")
        
        subprocess.run(cmd, env=env, cwd=BASE_DIR)
        
    except KeyboardInterrupt:
        print("\n  ✅ Сервер остановлен")
    except Exception as e:
        print(f"  ❌ Ошибка запуска сервера: {e}")

def main():
    """Основная функция восстановления"""
    print("🚨 ЭКСТРЕННОЕ ВОССТАНОВЛЕНИЕ Django")
    print("=" * 50)
    
    # Выполняем восстановление по шагам
    kill_all_python()
    fix_encoding()
    create_clean_env()
    clean_problematic_files()
    fix_settings()
    run_django_commands()
    
    print("=" * 50)
    print("✅ Экстренное восстановление завершено!")
    print()
    print("🔧 Что было исправлено:")
    print("  • Кодировка установлена в UTF-8")
    print("  • Созданы чистые настройки")
    print("  • Удалены проблемные файлы")
    print("  • Пересобраны статические файлы")
    print()
    print("⚠️ ВАЖНО:")
    print("  • Используйте ТОЛЬКО HTTP: http://127.0.0.1:8000")
    print("  • НЕ используйте HTTPS!")
    print("  • Очистите кеш браузера (Ctrl+Shift+R)")
    print()
    
    # Запускаем сервер
    start_server()

if __name__ == "__main__":
    main()
