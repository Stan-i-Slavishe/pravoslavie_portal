#!/usr/bin/env python
"""
Django Project Diagnostic and Recovery Script
Диагностирует и исправляет проблемы после Git отката
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"🔧 {text}")
    print(f"{'='*60}")

def print_step(step_num, text):
    print(f"\n{step_num}. {text}")

def run_command(command, description=""):
    """Выполняет команду и возвращает результат"""
    try:
        if description:
            print(f"   {description}")
        
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"   ✅ Успешно")
            return True, result.stdout
        else:
            print(f"   ❌ Ошибка: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"   ⏰ Таймаут команды")
        return False, "Timeout"
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
        return False, str(e)

def check_django_project():
    """Проверяет основные компоненты Django проекта"""
    print_header("ДИАГНОСТИКА DJANGO ПРОЕКТА")
    
    # Проверяем структуру проекта
    print_step(1, "Проверяем структуру проекта")
    
    required_files = [
        'manage.py',
        'config/settings.py',
        'config/urls.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
            print(f"   ❌ Отсутствует: {file_path}")
        else:
            print(f"   ✅ Найден: {file_path}")
    
    if missing_files:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: Отсутствуют файлы: {missing_files}")
        return False
    
    return True

def check_virtual_environment():
    """Проверяет виртуальное окружение"""
    print_step(2, "Проверяем виртуальное окружение")
    
    venv_path = Path('.venv')
    if not venv_path.exists():
        print("   ❌ Виртуальное окружение не найдено")
        return False
    
    activate_script = venv_path / 'Scripts' / 'activate.bat'
    if not activate_script.exists():
        print("   ❌ Скрипт активации не найден")
        return False
    
    print("   ✅ Виртуальное окружение найдено")
    return True

def check_database():
    """Проверяет подключение к базе данных"""
    print_step(3, "Проверяем базу данных")
    
    # Активируем виртуальное окружение и проверяем Django
    success, output = run_command(
        ".venv\\Scripts\\activate && python manage.py check --database default",
        "Проверяем подключение к БД"
    )
    
    return success

def check_migrations():
    """Проверяет миграции"""
    print_step(4, "Проверяем миграции")
    
    success, output = run_command(
        ".venv\\Scripts\\activate && python manage.py showmigrations",
        "Показываем статус миграций"
    )
    
    if success:
        print(f"   Статус миграций:\n{output}")
    
    return success

def fix_static_files():
    """Исправляет проблемы со статическими файлами"""
    print_step(5, "Исправляем статические файлы")
    
    # Удаляем папку staticfiles
    staticfiles_path = Path('staticfiles')
    if staticfiles_path.exists():
        try:
            shutil.rmtree(staticfiles_path)
            print("   ✅ Удалена папка staticfiles")
        except Exception as e:
            print(f"   ❌ Ошибка удаления staticfiles: {e}")
    
    # Пересобираем статические файлы
    success, output = run_command(
        ".venv\\Scripts\\activate && python manage.py collectstatic --noinput",
        "Пересобираем статические файлы"
    )
    
    return success

def clear_cache():
    """Очищает кеш Django"""
    print_step(6, "Очищаем кеш")
    
    cache_clear_command = """
.venv\\Scripts\\activate && python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
try:
    from django.core.cache import cache
    cache.clear()
    print('Кеш очищен')
except Exception as e:
    print(f'Ошибка очистки кеша: {e}')
"
    """
    
    success, output = run_command(cache_clear_command, "Очищаем Django кеш")
    
    return success

def check_dependencies():
    """Проверяет зависимости"""
    print_step(7, "Проверяем зависимости")
    
    success, output = run_command(
        ".venv\\Scripts\\activate && pip check",
        "Проверяем совместимость пакетов"
    )
    
    return success

def test_django_startup():
    """Тестируем запуск Django"""
    print_step(8, "Тестируем запуск Django")
    
    # Тест на проверку настроек
    success, output = run_command(
        ".venv\\Scripts\\activate && python manage.py check",
        "Проверяем настройки Django"
    )
    
    if not success:
        print(f"   Ошибки в настройках:\n{output}")
    
    return success

def emergency_fixes():
    """Экстренные исправления"""
    print_header("ЭКСТРЕННЫЕ ИСПРАВЛЕНИЯ")
    
    print_step(1, "Создаем резервную копию текущих настроек")
    
    # Копируем settings.py
    try:
        shutil.copy('config/settings.py', 'config/settings_backup.py')
        print("   ✅ Резервная копия settings.py создана")
    except Exception as e:
        print(f"   ❌ Ошибка создания резервной копии: {e}")
    
    print_step(2, "Временные исправления настроек")
    
    # Читаем текущие настройки
    try:
        with open('config/settings.py', 'r', encoding='utf-8') as f:
            settings_content = f.read()
        
        # Простые исправления
        fixes_applied = []
        
        # Убеждаемся что DEBUG = True для разработки
        if 'DEBUG = False' in settings_content:
            settings_content = settings_content.replace('DEBUG = False', 'DEBUG = True')
            fixes_applied.append("Включен DEBUG режим")
        
        # Добавляем localhost в ALLOWED_HOSTS если его нет
        if "'localhost'" not in settings_content and '"localhost"' not in settings_content:
            settings_content = settings_content.replace(
                "ALLOWED_HOSTS = []",
                "ALLOWED_HOSTS = ['localhost', '127.0.0.1']"
            )
            fixes_applied.append("Добавлен localhost в ALLOWED_HOSTS")
        
        # Записываем исправленные настройки
        with open('config/settings.py', 'w', encoding='utf-8') as f:
            f.write(settings_content)
        
        for fix in fixes_applied:
            print(f"   ✅ {fix}")
        
    except Exception as e:
        print(f"   ❌ Ошибка исправления настроек: {e}")

def main():
    """Основная функция диагностики"""
    print_header("ДИАГНОСТИКА И ВОССТАНОВЛЕНИЕ DJANGO ПРОЕКТА")
    print("Этот скрипт поможет диагностировать и исправить проблемы после Git отката")
    
    # Проверяем, что мы в правильной директории
    if not Path('manage.py').exists():
        print("❌ ОШИБКА: manage.py не найден. Запустите скрипт из корня Django проекта")
        return
    
    # Основная диагностика
    checks = [
        ("Структура проекта", check_django_project),
        ("Виртуальное окружение", check_virtual_environment),
        ("База данных", check_database),
        ("Миграции", check_migrations),
        ("Статические файлы", fix_static_files),
        ("Кеш", clear_cache),
        ("Зависимости", check_dependencies),
        ("Запуск Django", test_django_startup),
    ]
    
    failed_checks = []
    
    for check_name, check_func in checks:
        try:
            if not check_func():
                failed_checks.append(check_name)
        except Exception as e:
            print(f"   ❌ Исключение в проверке {check_name}: {e}")
            failed_checks.append(check_name)
    
    # Если есть критические ошибки, применяем экстренные исправления
    if failed_checks:
        print(f"\n❌ Обнаружены проблемы в: {', '.join(failed_checks)}")
        
        response = input("\nПрименить экстренные исправления? (y/n): ")
        if response.lower() in ['y', 'yes', 'д', 'да']:
            emergency_fixes()
            
            # Повторный тест запуска
            print_header("ПОВТОРНАЯ ПРОВЕРКА")
            if test_django_startup():
                print("\n🎉 Django успешно запускается!")
                print("\nДля запуска сервера используйте:")
                print("   .venv\\Scripts\\activate")
                print("   python manage.py runserver")
            else:
                print("\n❌ Все еще есть проблемы. Требуется ручная диагностика.")
    else:
        print("\n🎉 Все проверки пройдены успешно!")
        print("\nДля запуска сервера используйте:")
        print("   .venv\\Scripts\\activate")
        print("   python manage.py runserver")

if __name__ == "__main__":
    main()
