#!/usr/bin/env python3
"""
🔍 Скрипт проверки конфигурации после очистки
Проверяет, что все настроено правильно
"""

import os
import sys

def check_env_files():
    """Проверка наличия правильных .env файлов"""
    print("🔍 Проверка .env файлов...")
    
    required_files = ['.env.local', '.env.staging', '.env.production']
    unwanted_files = ['.env', '.env.lightweight', '.env.postgres_local', '.env.push_test', '.env.temp']
    
    all_good = True
    
    # Проверяем наличие нужных файлов
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} - найден")
        else:
            print(f"❌ {file_name} - НЕ НАЙДЕН!")
            all_good = False
    
    # Проверяем отсутствие ненужных файлов
    for file_name in unwanted_files:
        if os.path.exists(file_name):
            print(f"⚠️ {file_name} - всё ещё существует (должен быть удален)")
            all_good = False
        else:
            print(f"✅ {file_name} - удален")
    
    return all_good

def check_django_settings():
    """Проверка Django настроек"""
    print("\n🔍 Проверка Django настроек...")
    
    settings_files = [
        'config/settings.py',
        'config/settings_local.py',
        'config/settings_staging.py', 
        'config/settings_production.py'
    ]
    
    all_good = True
    
    for file_name in settings_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} - найден")
        else:
            print(f"❌ {file_name} - НЕ НАЙДЕН!")
            all_good = False
    
    return all_good

def test_environment_loading():
    """Тестирование загрузки разных окружений"""
    print("\n🧪 Тестирование загрузки окружений...")
    
    test_environments = ['local', 'staging', 'production']
    
    for env in test_environments:
        print(f"\n--- Тестирование {env.upper()} ---")
        
        # Устанавливаем переменную окружения
        os.environ['DJANGO_ENV'] = env
        
        try:
            # Пробуем импортировать настройки Django
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, '.')
            
            # Очищаем кеш модулей Django
            django_modules = [key for key in sys.modules.keys() if key.startswith('django') or key.startswith('config')]
            for module in django_modules:
                if module in sys.modules:
                    del sys.modules[module]
            
            # Импортируем настройки
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
            import django
            from django.conf import settings
            
            print(f"✅ {env}: Django настройки загружены")
            print(f"   DEBUG: {getattr(settings, 'DEBUG', 'НЕ ОПРЕДЕЛЕН')}")
            print(f"   ALLOWED_HOSTS: {getattr(settings, 'ALLOWED_HOSTS', 'НЕ ОПРЕДЕЛЕН')}")
            
            # Проверяем базу данных
            db_engine = settings.DATABASES.get('default', {}).get('ENGINE', 'НЕ ОПРЕДЕЛЕН')
            print(f"   DATABASE: {db_engine}")
            
        except Exception as e:
            print(f"❌ {env}: Ошибка загрузки - {e}")
    
    # Возвращаем обратно local для разработки
    os.environ['DJANGO_ENV'] = 'local'

def check_backup_exists():
    """Проверка наличия backup'а"""
    print("\n🔍 Проверка backup'ов...")
    
    if os.path.exists('backups/'):
        backups = [d for d in os.listdir('backups/') if d.startswith('WORKING_PRODUCTION_BACKUP')]
        if backups:
            latest_backup = sorted(backups)[-1]
            print(f"✅ Найден рабочий backup: backups/{latest_backup}")
            return True
        else:
            print("❌ Не найдены backup'ы рабочей конфигурации!")
            return False
    else:
        print("❌ Папка backups/ не найдена!")
        return False

def create_quick_start_guide():
    """Создание краткого руководства"""
    guide_content = """# 🚀 БЫСТРЫЙ СТАРТ ПОСЛЕ ОЧИСТКИ

## ✅ Что сделано:
- Убран хаос с .env файлами (было 7, стало 3)
- Созданы четкие окружения: local/staging/production
- Улучшена конфигурация settings_local.py
- Создан staging для безопасного тестирования
- Обновлен .gitignore

## 🔄 Как работать с окружениями:

### Локальная разработка (SQLite):
```bash
export DJANGO_ENV=local  # Linux/Mac
$env:DJANGO_ENV = "local"  # Windows
python manage.py runserver
```

### Локальная разработка (PostgreSQL):
```bash
# Измените в .env.local:
USE_SQLITE=False
# Укажите настройки PostgreSQL
```

### Тестирование на staging:
```bash
export DJANGO_ENV=staging
python manage.py check --deploy
python manage.py migrate
```

### Продакшн:
```bash
export DJANGO_ENV=production
python manage.py check --deploy
```

## 🎯 Следующие шаги:

### Шаг 1: Проверка (сейчас)
```bash
python check_environment.py  # Этот скрипт
python manage.py check
```

### Шаг 2: Настройка staging сервера (1-2 часа)
- Создать поддомен staging.dobrist.com
- Установить отдельную базу данных
- Настроить SSL сертификат

### Шаг 3: Тестирование процесса деплоя (30 минут)
- Протестировать изменения на staging
- Убедиться что все работает
- Только потом деплой на продакшн

### Шаг 4: OAuth интеграция (2-3 часа)
После стабильной архитектуры!

## 🚨 Аварийное восстановление:
Если что-то сломалось, используйте backup:
```bash
cp backups/WORKING_PRODUCTION_BACKUP_*/\\.env.production .env.production
export DJANGO_ENV=production
python manage.py check
```

## 📞 Проблемы?
1. Проверьте переменную DJANGO_ENV
2. Убедитесь что нужный .env файл существует
3. Проверьте логи Django
4. В крайнем случае - восстанавливайте из backup
"""
    
    with open('QUICK_START_AFTER_CLEANUP.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("📚 Создан гайд: QUICK_START_AFTER_CLEANUP.md")

def main():
    """Основная функция проверки"""
    print("🔍 ПРОВЕРКА КОНФИГУРАЦИИ ПОСЛЕ ОЧИСТКИ")
    print("=" * 50)
    
    # Проверяем все компоненты
    env_files_ok = check_env_files()
    django_settings_ok = check_django_settings()
    backup_exists = check_backup_exists()
    
    print("\n🧪 Тестирование окружений...")
    test_environment_loading()
    
    print("\n" + "=" * 50)
    
    # Создаем руководство
    create_quick_start_guide()
    
    # Итоговый отчет
    print("\n📊 ИТОГОВЫЙ ОТЧЕТ:")
    print(f"   .env файлы: {'✅ OK' if env_files_ok else '❌ ПРОБЛЕМЫ'}")
    print(f"   Django настройки: {'✅ OK' if django_settings_ok else '❌ ПРОБЛЕМЫ'}")
    print(f"   Backup рабочей конфигурации: {'✅ OK' if backup_exists else '❌ ПРОБЛЕМЫ'}")
    
    if env_files_ok and django_settings_ok and backup_exists:
        print("\n🎉 ВСЁ ГОТОВО! Архитектура стабилизирована!")
        print("\n🎯 Следующий шаг: настройка staging сервера")
        print("📖 См. QUICK_START_AFTER_CLEANUP.md")
    else:
        print("\n⚠️ Есть проблемы, нужно исправить перед продолжением")

if __name__ == "__main__":
    main()
