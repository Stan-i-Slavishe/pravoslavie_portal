#!/usr/bin/env python3
"""
Умный скрипт очистки временных и отладочных файлов
Удаляет только ненужные файлы из КОРНЯ проекта, не трогая директории
"""

import os
from pathlib import Path
import re

def smart_cleanup():
    """Умная очистка ненужных файлов в корне проекта"""
    
    project_root = Path("E:/pravoslavie_portal")
    
    # Паттерны ненужных файлов (только в корне!)
    cleanup_patterns = {
        'batch_files': {
            'pattern': '*.bat',
            'description': 'Batch скрипты для разработки'
        },
        'debug_scripts': {
            'pattern': 'diagnose_*.py',
            'description': 'Диагностические скрипты'
        },
        'test_scripts': {
            'pattern': 'test_*.py',
            'description': 'Тестовые скрипты'
        },
        'fix_scripts': {
            'pattern': 'fix_*.py',
            'description': 'Скрипты исправлений'
        },
        'check_scripts': {
            'pattern': 'check_*.py',
            'description': 'Скрипты проверок'
        },
        'temp_files': {
            'pattern': 'temp_*.py',
            'description': 'Временные файлы'
        },
        'setup_scripts': {
            'pattern': 'setup_*.py',
            'description': 'Скрипты настройки (кроме setup.py)'
        },
        'cleanup_scripts': {
            'pattern': 'clean*.py',
            'description': 'Скрипты очистки'
        },
        'sync_scripts': {
            'pattern': 'sync_*.py',
            'description': 'Скрипты синхронизации'
        },
        'backup_files': {
            'pattern': '*_backup*.py',
            'description': 'Резервные копии скриптов'
        }
    }
    
    # Файлы, которые НУЖНО СОХРАНИТЬ (белый список)
    keep_files = {
        'manage.py',           # Django управление
        'setup.py',            # Установка пакета (если есть)
        'requirements.txt',    # Зависимости
        'README.md',           # Документация
        '.gitignore',          # Git настройки
        '.env',                # Переменные окружения
        '.env.production',     # Продакшн настройки
        '.env.postgres_local', # Локальные настройки БД
        'wsgi.py',            # WSGI (если в корне)
        'asgi.py',            # ASGI (если в корне)
    }
    
    print("🧹 УМНАЯ ОЧИСТКА ПРОЕКТА")
    print("=" * 60)
    print("🎯 Анализируем ТОЛЬКО корень проекта (не директории)")
    print("=" * 60)
    
    # Собираем все файлы для удаления
    files_to_delete = {}
    total_files = 0
    
    # Проходим по всем паттернам
    for category, info in cleanup_patterns.items():
        pattern = info['pattern']
        description = info['description']
        
        # Находим файлы по паттерну
        matching_files = list(project_root.glob(pattern))
        
        # Фильтруем - только файлы (не директории) и не из белого списка
        category_files = []
        for file_path in matching_files:
            if (file_path.is_file() and 
                file_path.name not in keep_files and
                file_path.parent == project_root):  # Только корень!
                category_files.append(file_path)
        
        if category_files:
            files_to_delete[category] = {
                'files': category_files,
                'description': description
            }
            total_files += len(category_files)
    
    # Дополнительные специфичные файлы
    additional_patterns = [
        'apply_*.bat', 'run_*.bat', 'restart_*.bat', 'master_*.bat',
        'quick_*.py', 'force_*.py', 'emergency_*.py', 'auto_*.py',
        'final_*.py', 'simple_*.py', 'missing_*.py', 'remove_*.py',
        'validate_*.py', 'analyze_*.py', 'collect_*.py', 'create_*.py',
        'update_*.py', 'set_*.py', 'use_*.py', 'find_*.py'
    ]
    
    additional_files = []
    for pattern in additional_patterns:
        for file_path in project_root.glob(pattern):
            if (file_path.is_file() and 
                file_path.name not in keep_files and
                file_path.parent == project_root and
                file_path not in [f for cat in files_to_delete.values() for f in cat['files']]):
                additional_files.append(file_path)
    
    if additional_files:
        files_to_delete['additional'] = {
            'files': additional_files,
            'description': 'Дополнительные временные скрипты'
        }
        total_files += len(additional_files)
    
    # Показываем результаты анализа
    if not files_to_delete:
        print("✅ Временные файлы не найдены!")
        print("💡 Проект уже чистый")
        return
    
    print(f"🔍 Найдено {total_files} файлов для удаления:")
    print("=" * 60)
    
    total_size = 0
    for category, data in files_to_delete.items():
        files = data['files']
        description = data['description']
        
        print(f"\n📂 {description} ({len(files)} файлов):")
        category_size = 0
        
        for file_path in files[:10]:  # Показываем первые 10
            size = file_path.stat().st_size
            category_size += size
            print(f"   • {file_path.name} ({size} bytes)")
        
        if len(files) > 10:
            remaining_size = sum(f.stat().st_size for f in files[10:])
            category_size += remaining_size
            print(f"   • ... и еще {len(files) - 10} файлов")
        
        total_size += category_size
        print(f"   📊 Размер категории: {category_size:,} bytes")
    
    print("=" * 60)
    print(f"📊 ИТОГО: {total_files} файлов, {total_size:,} bytes")
    print("=" * 60)
    
    # Показываем что СОХРАНЯЕМ
    print("\n✅ ВАЖНЫЕ ФАЙЛЫ (будут сохранены):")
    important_files = []
    for file_name in keep_files:
        file_path = project_root / file_name
        if file_path.exists():
            important_files.append(file_name)
    
    if important_files:
        for file_name in important_files:
            print(f"   ✓ {file_name}")
    else:
        print("   (нет важных файлов в корне)")
    
    # Запрос подтверждения
    print("\n" + "=" * 60)
    print("⚠️  ВНИМАНИЕ: Файлы будут удалены БЕЗВОЗВРАТНО!")
    print("💡 Все .bat и временные .py файлы не влияют на работу сайта")
    print("🎯 Удаляются только файлы из КОРНЯ проекта")
    
    while True:
        choice = input(f"\n❓ Удалить {total_files} временных файлов? (y/n): ").strip().lower()
        if choice in ['y', 'yes', 'да', 'д']:
            break
        elif choice in ['n', 'no', 'нет', 'н']:
            print("❌ Очистка отменена")
            return
        else:
            print("⚠️  Введите 'y' для удаления или 'n' для отмены")
    
    # Удаляем файлы
    print(f"\n🗑️  Удаление {total_files} файлов...")
    deleted_count = 0
    deleted_size = 0
    errors = []
    
    for category, data in files_to_delete.items():
        files = data['files']
        description = data['description']
        
        print(f"\n📂 Удаляем: {description}")
        for file_path in files:
            try:
                size = file_path.stat().st_size
                file_path.unlink()
                print(f"   ✅ {file_path.name}")
                deleted_count += 1
                deleted_size += size
            except Exception as e:
                error_msg = f"❌ Ошибка удаления {file_path.name}: {e}"
                print(f"   {error_msg}")
                errors.append(error_msg)
    
    # Финальный отчет
    print("\n" + "=" * 60)
    print("📊 ОТЧЕТ ОБ ОЧИСТКЕ")
    print("=" * 60)
    print(f"✅ Удалено файлов: {deleted_count}")
    print(f"💾 Освобождено места: {deleted_size:,} bytes")
    
    if errors:
        print(f"⚠️  Ошибок: {len(errors)}")
        for error in errors:
            print(f"   {error}")
    
    if deleted_count > 0:
        print(f"\n🎉 Очистка завершена!")
        print(f"🧹 Корень проекта стал чище на {deleted_count} файлов")
        print(f"🚀 Django сайт продолжит работать нормально")
        print(f"📁 Все важные файлы и директории сохранены")
    else:
        print(f"\n😐 Файлы не были удалены")

if __name__ == "__main__":
    print("🧹 УМНАЯ ОЧИСТКА ПРОЕКТА")
    print("=" * 60)
    print("Этот скрипт найдет и удалит временные файлы ТОЛЬКО из корня проекта")
    print("=" * 60)
    
    smart_cleanup()
