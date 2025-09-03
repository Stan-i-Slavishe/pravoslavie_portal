#!/usr/bin/env python3
"""
🚨 АВАРИЙНЫЙ BACKUP ВСЕХ РАБОЧИХ НАСТРОЕК ПРОДАКШЕНА
Версия для Windows и любых систем
"""

import os
import shutil
import datetime
import subprocess
import sys

def create_backup():
    print("🚨 Создаем ПОЛНЫЙ backup рабочих настроек...")
    
    # Получаем текущую дату и время
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/WORKING_PRODUCTION_BACKUP_{timestamp}"
    
    # Создаем папку для backup
    os.makedirs(backup_dir, exist_ok=True)
    print(f"📁 Backup папка: {backup_dir}")
    
    # === КОПИРУЕМ ВСЕ КОНФИГУРАЦИОННЫЕ ФАЙЛЫ ===
    print("🔧 Копируем конфигурационные файлы...")
    
    # Список .env файлов для копирования
    env_files = [
        ('.env', 'dot_env_current'),
        ('.env.production', '.env.production'),
        ('.env.local', '.env.local'),
        ('.env.lightweight', '.env.lightweight'),
        ('.env.postgres_local', '.env.postgres_local'),
        ('.env.push_test', '.env.push_test'),
        ('.env.temp', '.env.temp')
    ]
    
    for source, dest in env_files:
        try:
            if os.path.exists(source):
                shutil.copy2(source, os.path.join(backup_dir, dest))
                print(f"✅ Скопирован: {source}")
            else:
                print(f"⚠️ Не найден: {source}")
        except Exception as e:
            print(f"❌ Ошибка копирования {source}: {e}")
    
    # Django settings
    try:
        if os.path.exists('config'):
            shutil.copytree('config', os.path.join(backup_dir, 'config_backup'))
            print("✅ Скопирована папка config/")
        else:
            print("⚠️ Папка config/ не найдена")
    except Exception as e:
        print(f"❌ Ошибка копирования config/: {e}")
    
    # Requirements
    try:
        if os.path.exists('requirements.txt'):
            shutil.copy2('requirements.txt', backup_dir)
            print("✅ Скопирован requirements.txt")
    except Exception as e:
        print(f"❌ Ошибка копирования requirements.txt: {e}")
    
    # === ЗАПИСЫВАЕМ СИСТЕМНУЮ ИНФОРМАЦИЮ ===
    print("📝 Записываем системную информацию...")
    
    system_info_path = os.path.join(backup_dir, 'system_info.txt')
    with open(system_info_path, 'w', encoding='utf-8') as f:
        f.write("=== СИСТЕМНАЯ ИНФОРМАЦИЯ ===\n")
        f.write(f"Дата создания backup: {datetime.datetime.now()}\n")
        f.write(f"Операционная система: {os.name}\n")
        f.write(f"Python версия: {sys.version}\n")
        f.write(f"Текущая папка: {os.getcwd()}\n\n")
        
        f.write("=== ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ===\n")
        for key in ['DJANGO_ENV', 'DEBUG', 'PATH']:
            value = os.environ.get(key, 'НЕ УСТАНОВЛЕНА')
            f.write(f"{key}: {value}\n")
        f.write("\n")
        
        # Пробуем получить информацию о Python пакетах
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                                  capture_output=True, text=True, timeout=30)
            f.write("=== УСТАНОВЛЕННЫЕ PYTHON ПАКЕТЫ ===\n")
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Ошибка получения списка пакетов: {e}\n")
        
        # Git информация
        try:
            result = subprocess.run(['git', 'branch'], capture_output=True, text=True, timeout=10)
            f.write(f"\n=== GIT ИНФОРМАЦИЯ ===\n")
            f.write(f"Ветки:\n{result.stdout}")
            
            result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                  capture_output=True, text=True, timeout=10)
            f.write(f"Последние коммиты:\n{result.stdout}")
        except Exception as e:
            f.write(f"Git информация недоступна: {e}\n")
    
    # === СОЗДАЕМ ИНСТРУКЦИЮ ПО ВОССТАНОВЛЕНИЮ ===
    restore_instructions = os.path.join(backup_dir, 'RESTORE_INSTRUCTIONS.md')
    with open(restore_instructions, 'w', encoding='utf-8') as f:
        f.write("""# 🚨 ИНСТРУКЦИЯ ПО ВОССТАНОВЛЕНИЮ РАБОЧЕЙ КОНФИГУРАЦИИ

## ЧТО ЗДЕСЬ НАХОДИТСЯ
Этот backup содержит ВСЕ рабочие настройки продакшена на момент создания.

## ФАЙЛЫ В BACKUP:
- `.env.production` - настройки продакшена (ГЛАВНЫЙ ФАЙЛ)
- `dot_env_current` - текущий .env файл
- `config_backup/` - все файлы Django настроек
- `requirements.txt` - список пакетов Python
- `system_info.txt` - информация о системе

## ЭКСТРЕННОЕ ВОССТАНОВЛЕНИЕ:

### Windows (PowerShell):
```powershell
# Восстанавливаем рабочие настройки
Copy-Item "backups\\WORKING_PRODUCTION_BACKUP_*\\.env.production" ".env.production"
Copy-Item "backups\\WORKING_PRODUCTION_BACKUP_*\\config_backup\\*" "config\\" -Recurse -Force

# Устанавливаем переменную окружения
$env:DJANGO_ENV = "production"

# Перезапускаем сервер (если используете)
# Restart-Service YourServiceName
```

### Linux/Mac:
```bash
# Восстанавливаем рабочие настройки
cp backups/WORKING_PRODUCTION_BACKUP_*/.env.production .env.production
cp -r backups/WORKING_PRODUCTION_BACKUP_*/config_backup/* config/

# Устанавливаем переменную окружения
export DJANGO_ENV=production

# Перезапускаем сервер
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## ⚠️ ВАЖНО:
- НЕ УДАЛЯЙТЕ этот backup!
- Перед любыми изменениями на продакшене создавайте новый backup
- Всегда тестируйте изменения на staging перед продакшеном

## КОНТРОЛЬНЫЙ СПИСОК ВОССТАНОВЛЕНИЯ:
1. ✅ Скопированы файлы конфигурации
2. ✅ Установлена переменная DJANGO_ENV=production
3. ✅ Перезапущен веб-сервер
4. ✅ Проверена доступность сайта
5. ✅ Проверены логи на ошибки
""")
    
    # === СОЗДАЕМ КРАТКУЮ СПРАВКУ ===
    quick_ref_path = os.path.join(backup_dir, 'QUICK_REFERENCE.txt')
    with open(quick_ref_path, 'w', encoding='utf-8') as f:
        f.write("""🚨 БЫСТРАЯ СПРАВКА - АВАРИЙНОЕ ВОССТАНОВЛЕНИЕ

ЕСЛИ САЙТ НЕ РАБОТАЕТ:

Windows:
1. Copy-Item "этот_backup\\.env.production" ".env.production"
2. $env:DJANGO_ENV = "production"
3. python manage.py runserver (для теста)

Linux:
1. cp этот_backup/.env.production .env.production
2. export DJANGO_ENV=production
3. sudo systemctl restart gunicorn && sudo systemctl restart nginx

ПРОВЕРКА:
- python manage.py check
- python manage.py migrate --check
- Логи сервера

ПОМОЩЬ: найти последний working backup в папке backups/
""")
    
    print("✅ Backup создан успешно!")
    print(f"📁 Местоположение: {backup_dir}")
    print("")
    print("🔒 ВАЖНО: Этот backup содержит рабочие настройки продакшена!")
    print(f"📋 Инструкции по восстановлению: {restore_instructions}")
    print("")
    print("🎯 Следующий шаг: очистка лишних .env файлов")
    
    return backup_dir

if __name__ == "__main__":
    backup_path = create_backup()
    print(f"\n🎉 Backup завершен: {backup_path}")
