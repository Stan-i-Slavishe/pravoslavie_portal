import os
import django
from django.conf import settings

# Добавляем путь к проекту
import sys
sys.path.append('E:/pravoslavie_portal')

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def diagnose_profile_form():
    """Диагностика проблем с формой профиля"""
    
    print("🔍 ДИАГНОСТИКА ПРОБЛЕМ С ФОРМОЙ ПРОФИЛЯ")
    print("=" * 50)
    
    # 1. Проверяем существование файлов
    print("\n1. Проверка файлов:")
    profile_edit_path = "accounts/templates/accounts/profile_edit.html"
    if os.path.exists(profile_edit_path):
        print(f"✓ {profile_edit_path} существует")
        
        # Проверяем содержимое файла
        with open(profile_edit_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"   - Размер файла: {len(content)} символов")
        print(f"   - Содержит CSS: {'<style>' in content}")
        print(f"   - Содержит JavaScript: {'<script>' in content}")
        print(f"   - Содержит pointer-events: {'pointer-events' in content}")
        print(f"   - Содержит crispy forms: {'crispy_forms_tags' in content}")
        
    else:
        print(f"❌ {profile_edit_path} НЕ НАЙДЕН!")
    
    # 2. Проверяем модель UserProfile
    print("\n2. Проверка модели UserProfile:")
    try:
        from accounts.models import UserProfile
        fields = [field.name for field in UserProfile._meta.fields]
        print(f"✓ Модель UserProfile загружена")
        print(f"   - Количество полей: {len(fields)}")
        print(f"   - Поля: {', '.join(fields[:10])}...")
    except ImportError as e:
        print(f"❌ Ошибка импорта UserProfile: {e}")
    
    # 3. Проверяем форму UserProfileForm
    print("\n3. Проверка формы UserProfileForm:")
    try:
        from accounts.forms import UserProfileForm
        form = UserProfileForm()
        print(f"✓ Форма UserProfileForm загружена")
        print(f"   - Количество полей в форме: {len(form.fields)}")
        print(f"   - Поля формы: {', '.join(list(form.fields.keys())[:10])}...")
        
        # Проверяем виджеты полей
        problematic_fields = []
        for field_name, field in form.fields.items():
            widget_class = field.widget.__class__.__name__
            if hasattr(field.widget, 'attrs'):
                attrs = field.widget.attrs
                if 'pointer-events' in str(attrs):
                    problematic_fields.append(field_name)
        
        if problematic_fields:
            print(f"   ⚠️ Поля с pointer-events проблемами: {problematic_fields}")
        else:
            print(f"   ✓ Виджеты полей выглядят нормально")
            
    except ImportError as e:
        print(f"❌ Ошибка импорта UserProfileForm: {e}")
    
    # 4. Проверяем URL-маршруты
    print("\n4. Проверка URL-маршрутов:")
    try:
        from django.urls import reverse
        profile_edit_url = reverse('accounts:profile_edit')
        print(f"✓ URL профиля найден: {profile_edit_url}")
    except Exception as e:
        print(f"❌ Ошибка URL: {e}")
    
    # 5. Проверяем статические файлы
    print("\n5. Проверка статических файлов:")
    static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
    print(f"   - STATICFILES_DIRS: {static_dirs}")
    
    # Проверяем Bootstrap
    bootstrap_css_found = False
    for static_dir in static_dirs:
        if os.path.exists(static_dir):
            for root, dirs, files in os.walk(static_dir):
                if any('bootstrap' in f.lower() for f in files):
                    bootstrap_css_found = True
                    break
    
    if bootstrap_css_found:
        print("   ✓ Bootstrap файлы найдены")
    else:
        print("   ⚠️ Bootstrap файлы не найдены в статических директориях")
    
    # 6. Возможные проблемы и решения
    print("\n6. ВОЗМОЖНЫЕ ПРИЧИНЫ ПРОБЛЕМЫ:")
    print("   1. CSS overlay блокирует клики на поля")
    print("   2. JavaScript перехватывает события")
    print("   3. Bootstrap CSS конфликты")
    print("   4. Crispy Forms добавляет свои стили")
    print("   5. Z-index проблемы с элементами")
    
    print("\n7. РЕКОМЕНДУЕМЫЕ РЕШЕНИЯ:")
    print("   1. Запустите fix_profile_form_fields.bat")
    print("   2. Добавьте pointer-events: auto !important; для полей")
    print("   3. Проверьте браузерную консоль на ошибки JavaScript")
    print("   4. Обновите страницу с принудительной перезагрузкой (Ctrl+F5)")
    
    print("\n" + "=" * 50)
    print("🔧 АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ:")
    print("   Запустите: fix_profile_form_fields.bat")
    print("   Или используйте исправленный файл: profile_edit_fixed.html")

if __name__ == "__main__":
    diagnose_profile_form()
