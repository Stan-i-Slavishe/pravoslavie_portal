#!/usr/bin/env python
"""
🔄 Полный откат изменений после fix_browser_errors.bat
"""
import os
import sys
import shutil
from pathlib import Path

# Путь к проекту
BASE_DIR = Path(__file__).resolve().parent

def rollback_base_html():
    """Отменяем изменения в base.html"""
    print("🔄 Откатываем изменения в base.html...")
    
    base_html_path = BASE_DIR / 'templates' / 'base.html'
    
    if base_html_path.exists():
        # Читаем текущий файл
        with open(base_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Убираем подключение error-filter.js
        if 'error-filter.js' in content:
            content = content.replace(
                '    <!-- Фильтр ошибок (загружается первым) -->\n    <script src="{% static \'js/error-filter.js\' %}"></script>\n    \n',
                ''
            )
            
            # Записываем обратно
            with open(base_html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  ✅ Убрано подключение error-filter.js из base.html")
        else:
            print("  ℹ️ error-filter.js не найден в base.html")
    else:
        print("  ⚠️ Файл base.html не найден")

def disable_error_filter():
    """Отключаем или переименовываем error-filter.js"""
    print("🚫 Отключаем error-filter.js...")
    
    error_filter_path = BASE_DIR / 'static' / 'js' / 'error-filter.js'
    
    if error_filter_path.exists():
        # Переименовываем файл, чтобы он не загружался
        disabled_path = BASE_DIR / 'static' / 'js' / 'error-filter.js.disabled'
        error_filter_path.rename(disabled_path)
        print("  ✅ error-filter.js переименован в error-filter.js.disabled")
    else:
        print("  ℹ️ error-filter.js не найден")

def clean_static_files():
    """Очищаем статические файлы"""
    print("🧹 Очищаем статические файлы...")
    
    staticfiles_dir = BASE_DIR / 'staticfiles'
    
    if staticfiles_dir.exists():
        shutil.rmtree(staticfiles_dir)
        print("  ✅ Папка staticfiles удалена")
    else:
        print("  ℹ️ Папка staticfiles не найдена")

def restore_settings():
    """Восстанавливаем настройки окружения"""
    print("⚙️ Восстанавливаем настройки...")
    
    env_file = BASE_DIR / '.env'
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Включаем DEBUG обратно
        if 'DEBUG=False' in content:
            content = content.replace('DEBUG=False', 'DEBUG=True')
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  ✅ DEBUG=True восстановлен в .env")
        else:
            print("  ℹ️ DEBUG уже включен или не найден")
    else:
        print("  ⚠️ Файл .env не найден")

def clear_django_cache():
    """Очищаем кеш Django"""
    print("🗑️ Очищаем кеш Django...")
    
    try:
        # Настройка Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        import django
        django.setup()
        
        from django.core.cache import cache
        cache.clear()
        print("  ✅ Кеш Django очищен")
    except Exception as e:
        print(f"  ⚠️ Не удалось очистить кеш Django: {e}")

def remove_problem_files():
    """Удаляем проблемные файлы"""
    print("🗂️ Удаляем проблемные файлы...")
    
    problem_files = [
        BASE_DIR / 'staticfiles' / 'js' / 'error-filter.js',
        BASE_DIR / 'staticfiles' / 'js' / 'error-filter.*.js',
    ]
    
    for file_path in problem_files:
        if file_path.exists():
            file_path.unlink()
            print(f"  ✅ Удален {file_path.name}")

def main():
    """Основная функция отката"""
    print("🔄 Начинаем полный откат изменений...")
    print("=" * 50)
    
    # Выполняем откат по шагам
    rollback_base_html()
    disable_error_filter()
    clean_static_files()
    restore_settings()
    remove_problem_files()
    clear_django_cache()
    
    print("=" * 50)
    print("✅ Откат завершен успешно!")
    print()
    print("📋 Что было отменено:")
    print("  • Убрано подключение error-filter.js")
    print("  • Отключен агрессивный фильтр ошибок")
    print("  • Очищены статические файлы")
    print("  • Включен DEBUG режим")
    print("  • Очищен кеш Django")
    print()
    print("🚀 Следующие шаги:")
    print("  1. Перезапустите Django сервер")
    print("  2. Сделайте жесткую перезагрузку браузера (Ctrl+Shift+R)")
    print("  3. Проверьте работу сайта")
    print()
    print("💡 Если проблемы остались:")
    print("  • Перезагрузите компьютер")
    print("  • Очистите кеш браузера вручную")
    print("  • Проверьте логи Django на ошибки")

if __name__ == "__main__":
    main()
    input("\nНажмите Enter для выхода...")
