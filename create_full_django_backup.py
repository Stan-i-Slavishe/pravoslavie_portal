#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полный бэкап через Django (без использования pg_dump)
"""

import os
import sys
import django
import shutil
import json
from datetime import datetime

# Настройка Django
os.environ['DJANGO_ENV'] = 'local'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.management import call_command
from django.db import connection

def create_django_backup():
    """Создание бэкапа через Django"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = f"backups/django_backup_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    print(f"Создание полного Django бэкапа...")
    print(f"Папка: {backup_dir}")
    print()
    
    # 1. Полный дамп всех данных Django
    print("Создание полного Django fixture...")
    full_fixture = os.path.join(backup_dir, 'full_data.json')
    
    try:
        with open(full_fixture, 'w', encoding='utf-8') as f:
            call_command('dumpdata', 
                        natural_foreign=True,
                        natural_primary=True,
                        indent=2,
                        stdout=f)
        print(f"Полный fixture создан: {full_fixture}")
        
        # Проверяем размер файла
        size = os.path.getsize(full_fixture)
        print(f"Размер: {size:,} байт ({size/1024/1024:.1f} MB)")
        
    except Exception as e:
        print(f"Ошибка создания полного fixture: {e}")
    
    # 2. Дампы по приложениям
    print("\nСоздание дампов по приложениям...")
    
    apps = ['auth', 'core', 'stories', 'books', 'shop', 'fairy_tales', 'accounts', 'subscriptions']
    
    for app in apps:
        try:
            app_fixture = os.path.join(backup_dir, f'{app}_data.json')
            call_command('dumpdata', app, 
                        natural_foreign=True,
                        natural_primary=True, 
                        indent=2,
                        output=app_fixture)
            
            if os.path.exists(app_fixture):
                size = os.path.getsize(app_fixture)
                print(f"  {app}: {size:,} байт")
            
        except Exception as e:
            print(f"  {app}: ошибка - {e}")
    
    # 3. Информация о базе данных
    print("\nСоздание информации о БД...")
    
    db_info = {}
    try:
        with connection.cursor() as cursor:
            # Версия PostgreSQL
            cursor.execute("SELECT version();")
            db_info['postgresql_version'] = cursor.fetchone()[0]
            
            # Информация о таблицах
            cursor.execute("""
                SELECT table_name, 
                       (SELECT COUNT(*) FROM information_schema.columns 
                        WHERE table_name = t.table_name AND table_schema = 'public') as column_count
                FROM information_schema.tables t 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            
            tables = []
            for table_name, column_count in cursor.fetchall():
                cursor.execute(f'SELECT COUNT(*) FROM "{table_name}";')
                row_count = cursor.fetchone()[0]
                tables.append({
                    'name': table_name,
                    'columns': column_count,
                    'rows': row_count
                })
            
            db_info['tables'] = tables
            
            # Общая статистика
            cursor.execute("""
                SELECT COUNT(*) as table_count,
                       SUM(column_count) as total_columns
                FROM (
                    SELECT table_name,
                           (SELECT COUNT(*) FROM information_schema.columns 
                            WHERE table_name = t.table_name AND table_schema = 'public') as column_count
                    FROM information_schema.tables t 
                    WHERE table_schema = 'public'
                ) stats;
            """)
            
            stats = cursor.fetchone()
            db_info['statistics'] = {
                'total_tables': stats[0],
                'total_columns': stats[1],
                'total_rows': sum(table['rows'] for table in tables)
            }
            
    except Exception as e:
        print(f"Ошибка получения информации о БД: {e}")
        db_info['error'] = str(e)
    
    # Сохраняем информацию о БД
    db_info_file = os.path.join(backup_dir, 'database_info.json')
    with open(db_info_file, 'w', encoding='utf-8') as f:
        json.dump(db_info, f, ensure_ascii=False, indent=2)
    
    print(f"Информация о БД сохранена: {db_info_file}")
    
    # 4. Копирование медиа-файлов
    print("\nКопирование медиа-файлов...")
    
    media_src = 'media'
    media_dst = os.path.join(backup_dir, 'media')
    
    if os.path.exists(media_src):
        shutil.copytree(media_src, media_dst)
        
        # Подсчет файлов в media
        media_count = 0
        media_size = 0
        for root, dirs, files in os.walk(media_dst):
            media_count += len(files)
            for file in files:
                media_size += os.path.getsize(os.path.join(root, file))
        
        print(f"Медиа-файлы скопированы: {media_count} файлов, {media_size/1024/1024:.1f} MB")
    else:
        print("Папка media не найдена")
        media_count = 0
        media_size = 0
    
    # 5. Создание подробного отчета
    print("\nСоздание отчета о бэкапе...")
    
    report_file = os.path.join(backup_dir, 'backup_report.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("ПОЛНЫЙ БЭКАП DJANGO - ПРАВОСЛАВНЫЙ ПОРТАЛ\n")
        f.write("="*60 + "\n\n")
        f.write(f"Дата создания: {datetime.now()}\n")
        f.write(f"Метод: Django dumpdata (без pg_dump)\n\n")
        
        f.write("СОДЕРЖИМОЕ БЭКАПА:\n")
        f.write("-" * 30 + "\n")
        f.write("• full_data.json - полный дамп всех данных Django\n")
        f.write("• *_data.json - дампы по приложениям\n") 
        f.write("• database_info.json - информация о структуре БД\n")
        f.write("• media/ - копия всех медиа-файлов\n")
        f.write("• backup_report.txt - этот отчет\n\n")
        
        if 'statistics' in db_info:
            stats = db_info['statistics']
            f.write("СТАТИСТИКА БАЗЫ ДАННЫХ:\n")
            f.write("-" * 30 + "\n")
            f.write(f"• Таблиц: {stats['total_tables']}\n")
            f.write(f"• Столбцов: {stats['total_columns']}\n") 
            f.write(f"• Записей: {stats['total_rows']:,}\n\n")
        
        f.write("МЕДИА-ФАЙЛЫ:\n")
        f.write("-" * 30 + "\n")
        f.write(f"• Файлов: {media_count:,}\n")
        f.write(f"• Размер: {media_size/1024/1024:.1f} MB\n\n")
        
        # Размеры файлов бэкапа
        f.write("РАЗМЕРЫ ФАЙЛОВ БЭКАПА:\n")
        f.write("-" * 30 + "\n")
        
        total_backup_size = 0
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                if file != 'backup_report.txt':  # Исключаем сам отчет
                    filepath = os.path.join(root, file)
                    size = os.path.getsize(filepath)
                    total_backup_size += size
                    rel_path = os.path.relpath(filepath, backup_dir)
                    f.write(f"• {rel_path}: {size:,} байт\n")
        
        f.write(f"\nОБЩИЙ РАЗМЕР: {total_backup_size:,} байт ({total_backup_size/1024/1024:.1f} MB)\n\n")
        
        f.write("ВОССТАНОВЛЕНИЕ:\n")
        f.write("-" * 30 + "\n")
        f.write("1. Создать новую базу данных PostgreSQL\n")
        f.write("2. Применить миграции Django: python manage.py migrate\n")
        f.write("3. Загрузить данные: python manage.py loaddata full_data.json\n")
        f.write("4. Скопировать медиа-файлы в папку media/\n")
        f.write("5. Создать суперпользователя: python manage.py createsuperuser\n\n")
        
        f.write("ПРИМЕЧАНИЯ:\n")
        f.write("-" * 30 + "\n")
        f.write("• Этот бэкап создан методом Django dumpdata\n")
        f.write("• Включает все данные приложений и медиа-файлы\n")
        f.write("• Не включает системные таблицы PostgreSQL\n")
        f.write("• Для полного бэкапа БД используйте pg_dump отдельно\n")
    
    print(f"Отчет создан: {report_file}")
    
    # Итоговая статистика
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(backup_dir):
        for file in files:
            filepath = os.path.join(root, file)
            total_size += os.path.getsize(filepath)
            file_count += 1
    
    print("\n" + "="*60)
    print("БЭКАП ЗАВЕРШЕН УСПЕШНО!")
    print("="*60)
    print(f"Расположение: {backup_dir}")
    print(f"Файлов создано: {file_count:,}")
    print(f"Общий размер: {total_size:,} байт ({total_size/1024/1024:.1f} MB)")
    
    if 'statistics' in db_info:
        print(f"Записей в БД: {db_info['statistics']['total_rows']:,}")
    
    print(f"Медиа-файлов: {media_count:,}")
    
    return backup_dir

if __name__ == "__main__":
    try:
        backup_location = create_django_backup()
        print(f"\nБэкап успешно создан в: {backup_location}")
    except Exception as e:
        print(f"\nОшибка создания бэкапа: {e}")
        import traceback
        traceback.print_exc()
