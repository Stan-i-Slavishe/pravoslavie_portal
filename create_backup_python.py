#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт создания бэкапа PostgreSQL с аутентификацией
"""

import os
import subprocess
import sys
from datetime import datetime
import shutil

def create_backup():
    """Создание полного бэкапа PostgreSQL"""
    
    # Настройки подключения
    db_settings = {
        'host': 'localhost',
        'port': '5432',
        'database': 'pravoslavie_local_db',
        'user': 'pravoslavie_user',
        'password': 'local_strong_password_2024'
    }
    
    # Установка переменных окружения для pg_dump
    os.environ['PGPASSWORD'] = db_settings['password']
    
    # Создание папки бэкапа
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = f"backups/postgresql_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    print(f"Создание бэкапа PostgreSQL...")
    print(f"База данных: {db_settings['database']}")
    print(f"Пользователь: {db_settings['user']}")
    print(f"Папка бэкапа: {backup_dir}")
    print()
    
    # 1. SQL дамп
    sql_file = os.path.join(backup_dir, 'database.sql')
    print("Создание SQL дампа...")
    
    try:
        cmd = [
            'pg_dump',
            '-h', db_settings['host'],
            '-p', db_settings['port'], 
            '-U', db_settings['user'],
            '-d', db_settings['database'],
            '-f', sql_file,
            '--verbose',
            '--no-owner',
            '--no-privileges'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ SQL дамп создан: {sql_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка создания SQL дампа: {e}")
        print(f"Вывод: {e.stderr}")
    
    # 2. Сжатый дамп
    dump_file = os.path.join(backup_dir, 'database.dump')
    print("Создание сжатого дампа...")
    
    try:
        cmd = [
            'pg_dump',
            '-h', db_settings['host'],
            '-p', db_settings['port'],
            '-U', db_settings['user'], 
            '-d', db_settings['database'],
            '-f', dump_file,
            '--format=custom',
            '--compress=9',
            '--verbose',
            '--no-owner',
            '--no-privileges'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Сжатый дамп создан: {dump_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Ошибка создания сжатого дампа: {e}")
    
    # 3. Копирование медиа-файлов
    media_src = 'media'
    media_dst = os.path.join(backup_dir, 'media')
    
    if os.path.exists(media_src):
        print("Копирование медиа-файлов...")
        shutil.copytree(media_src, media_dst)
        print(f"✅ Медиа-файлы скопированы в {media_dst}")
    else:
        print("⚠️ Папка media не найдена")
    
    # 4. Django fixture
    print("Создание Django fixture...")
    django_file = os.path.join(backup_dir, 'django_data.json')
    
    try:
        os.environ['DJANGO_ENV'] = 'local'
        cmd = [
            sys.executable, 'manage.py', 'dumpdata',
            '--natural-foreign', '--natural-primary',
            '--settings=config.settings_local',
            '-o', django_file
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ Django fixture создан: {django_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Ошибка создания Django fixture: {e}")
    
    # 5. Создание информационного файла
    info_file = os.path.join(backup_dir, 'backup_info.txt')
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write("POSTGRESQL BACKUP - PRAVOSLAVIE PORTAL\n")
        f.write("="*50 + "\n\n")
        f.write(f"Создан: {datetime.now()}\n")
        f.write(f"База данных: {db_settings['database']}\n")
        f.write(f"Пользователь: {db_settings['user']}\n")
        f.write(f"Хост: {db_settings['host']}\n")
        f.write(f"Порт: {db_settings['port']}\n\n")
        
        f.write("СОДЕРЖИМОЕ БЭКАПА:\n")
        f.write("- database.sql     : SQL дамп (читаемый)\n")
        f.write("- database.dump    : Сжатый дамп (для pg_restore)\n")
        f.write("- django_data.json : Django fixture\n")
        f.write("- media/           : Медиа-файлы\n\n")
        
        f.write("КОМАНДЫ ВОССТАНОВЛЕНИЯ:\n")
        f.write("1. Из SQL дампа:\n")
        f.write(f"   psql -h {db_settings['host']} -U {db_settings['user']} -d {db_settings['database']} -f database.sql\n\n")
        f.write("2. Из сжатого дампа:\n")
        f.write(f"   pg_restore -h {db_settings['host']} -U {db_settings['user']} -d {db_settings['database']} database.dump\n\n")
        f.write("3. Django fixture:\n")
        f.write("   python manage.py loaddata django_data.json\n\n")
        
        # Информация о размерах файлов
        f.write("РАЗМЕРЫ ФАЙЛОВ:\n")
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                if file != 'backup_info.txt':  # Не включаем сам info файл
                    filepath = os.path.join(root, file)
                    size = os.path.getsize(filepath)
                    rel_path = os.path.relpath(filepath, backup_dir)
                    f.write(f"{rel_path}: {size:,} байт\n")
    
    print(f"✅ Информационный файл создан: {info_file}")
    
    # Очистка переменной окружения с паролем
    if 'PGPASSWORD' in os.environ:
        del os.environ['PGPASSWORD']
    
    # Итоги
    print("\n" + "="*50)
    print("БЭКАП ЗАВЕРШЕН УСПЕШНО!")
    print("="*50)
    print(f"📁 Расположение: {backup_dir}")
    print("\nСодержимое:")
    
    total_size = 0
    for root, dirs, files in os.walk(backup_dir):
        for file in files:
            filepath = os.path.join(root, file)
            size = os.path.getsize(filepath)
            total_size += size
            rel_path = os.path.relpath(filepath, backup_dir)
            print(f"   📄 {rel_path}: {size:,} байт")
    
    print(f"\n📊 Общий размер бэкапа: {total_size:,} байт ({total_size/1024/1024:.1f} MB)")
    
    print("\n💡 Рекомендации:")
    print("   • Храните бэкапы в безопасном месте")
    print("   • Регулярно создавайте новые бэкапы") 
    print("   • Тестируйте процедуру восстановления")
    print("   • Используйте внешние накопители")
    
    return backup_dir

if __name__ == "__main__":
    try:
        backup_location = create_backup()
        print(f"\n🎉 Бэкап успешно создан в: {backup_location}")
    except Exception as e:
        print(f"\n❌ Ошибка создания бэкапа: {e}")
        import traceback
        traceback.print_exc()