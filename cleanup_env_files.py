#!/usr/bin/env python3
"""
🧹 Скрипт очистки .env файлов
Безопасно удаляет лишние файлы и оставляет только 3 нужных
"""

import os
import shutil
from datetime import datetime

def cleanup_env_files():
    print("🧹 Начинаем очистку .env файлов...")
    
    # Создаем backup папку для удаляемых файлов (на всякий случай)
    backup_dir = f"backups/deleted_env_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    print(f"📁 Создана папка для удаляемых файлов: {backup_dir}")
    
    # Список файлов для удаления
    files_to_remove = [
        '.env',
        '.env.lightweight', 
        '.env.postgres_local',
        '.env.push_test',
        '.env.temp'
    ]
    
    removed_count = 0
    
    # Удаляем лишние файлы (с backup'ом)
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            # Создаем backup перед удалением
            shutil.copy2(file_name, os.path.join(backup_dir, file_name))
            os.remove(file_name)
            print(f"❌ Удален: {file_name}")
            removed_count += 1
        else:
            print(f"⚠️ Не найден: {file_name}")
    
    # Заменяем старый .env.local на новый улучшенный
    if os.path.exists('.env.local.new'):
        if os.path.exists('.env.local'):
            shutil.copy2('.env.local', os.path.join(backup_dir, '.env.local.old'))
        shutil.move('.env.local.new', '.env.local')
        print("✅ .env.local заменен на улучшенную версию")
    
    # Заменяем старый settings_local.py
    if os.path.exists('config/settings_local_new.py'):
        if os.path.exists('config/settings_local.py'):
            shutil.copy2('config/settings_local.py', os.path.join(backup_dir, 'settings_local.py.old'))
        shutil.move('config/settings_local_new.py', 'config/settings_local.py')
        print("✅ config/settings_local.py заменен на улучшенную версию")
    
    # Проверяем результат
    print("\n📋 РЕЗУЛЬТАТ ОЧИСТКИ:")
    env_files = [f for f in os.listdir('.') if f.startswith('.env')]
    for env_file in sorted(env_files):
        if env_file in ['.env.local', '.env.staging', '.env.production']:
            print(f"✅ {env_file} - ОСТАЛСЯ")
        else:
            print(f"❓ {env_file} - неожиданный файл")
    
    print(f"\n📊 СТАТИСТИКА:")
    print(f"   Удалено файлов: {removed_count}")
    print(f"   Backup создан в: {backup_dir}")
    print(f"   Осталось .env файлов: {len([f for f in env_files if f in ['.env.local', '.env.staging', '.env.production']])}")
    
    return backup_dir

def update_gitignore():
    """Обновляем .gitignore для защиты конфиденциальных данных"""
    print("\n🔒 Обновляем .gitignore...")
    
    gitignore_content = """
# === КОНФИДЕНЦИАЛЬНЫЕ ФАЙЛЫ ===
.env.local
.env.staging
.env.production
.env.*

# === БАЗЫ ДАННЫХ ===
db.sqlite3
*.db

# === ЛОГИ ===
logs/
*.log

# === PYTHON ===
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# === DJANGO ===
staticfiles/
media/uploads/
local_settings.py

# === IDE ===
.vscode/
.idea/
*.swp
*.swo

# === СИСТЕМА ===
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content.strip())
    
    print("✅ .gitignore обновлен")

def create_environment_docs():
    """Создаем документацию по окружениям"""
    print("\n📚 Создаем документацию...")
    
    doc_content = """# 📁 Конфигурация окружений

## 🎯 Принцип работы

Проект использует **3 четких окружения**:

### 🔧 `.env.local` - Локальная разработка
- SQLite база данных (по умолчанию)
- DEBUG=True
- Письма в консоль
- Тестовые API ключи
- Возможность переключения на PostgreSQL

### 🧪 `.env.staging` - Тестирование
- PostgreSQL (отдельная база!)
- DEBUG=False
- Полные настройки безопасности
- Тестовые API ключи
- Домен: staging.dobrist.com

### 🚀 `.env.production` - Продакшн
- PostgreSQL продакшена
- DEBUG=False
- Максимальная безопасность
- Реальные API ключи
- Домен: dobrist.com

## 🔄 Как переключаться между окружениями

### Windows:
```powershell
# Локальная разработка
$env:DJANGO_ENV = "local"

# Staging тестирование
$env:DJANGO_ENV = "staging"

# Продакшн
$env:DJANGO_ENV = "production"
```

### Linux/Mac:
```bash
# Локальная разработка
export DJANGO_ENV=local

# Staging тестирование
export DJANGO_ENV=staging

# Продакшн
export DJANGO_ENV=production
```

## ⚙️ Гибкие настройки .env.local

### SQLite (по умолчанию):
```env
USE_SQLITE=True
```

### PostgreSQL для тестирования:
```env
USE_SQLITE=False
DB_NAME=pravoslavie_portal_dev
DB_USER=postgres
DB_PASSWORD=your_password
```

## 🚨 Правила безопасности

1. **НИКОГДА** не коммитьте .env файлы в Git!
2. **ВСЕГДА** тестируйте на staging перед продакшеном
3. **ИСПОЛЬЗУЙТЕ** разные пароли для каждого окружения
4. **СОЗДАВАЙТЕ** backup перед изменениями

## 🛠️ Команды для проверки

```bash
# Проверить текущие настройки
python manage.py check

# Проверить настройки продакшена
python manage.py check --deploy

# Посмотреть какое окружение загружено
python manage.py shell -c "from django.conf import settings; print(f'Environment: {settings.ENVIRONMENT}')"
```
"""
    
    with open('ENVIRONMENTS.md', 'w', encoding='utf-8') as f:
        f.write(doc_content)
    
    print("✅ Создана документация ENVIRONMENTS.md")

def main():
    """Основная функция очистки"""
    print("🚀 ЗАПУСК ОЧИСТКИ .ENV ФАЙЛОВ")
    print("=" * 50)
    
    # Проверяем, что мы в правильной директории
    if not os.path.exists('manage.py'):
        print("❌ Ошибка: запустите скрипт из корневой папки Django проекта")
        return
    
    # Выполняем очистку
    backup_dir = cleanup_env_files()
    update_gitignore()
    create_environment_docs()
    
    print("\n" + "=" * 50)
    print("✅ ОЧИСТКА ЗАВЕРШЕНА УСПЕШНО!")
    print(f"📁 Backup удаленных файлов: {backup_dir}")
    print("\n🎯 СЛЕДУЮЩИЕ ШАГИ:")
    print("1. Проверьте настройки: python manage.py check")
    print("2. Запустите локальный сервер: python manage.py runserver")
    print("3. Настройте staging сервер")
    print("4. После тестирования staging - приступайте к OAuth")
    print("\n📚 Документация: ENVIRONMENTS.md")

if __name__ == "__main__":
    main()
