import os
import sys
import django

print("🗑️ Полное удаление православного календаря из проекта")
print("=" * 55)

try:
    # Настройка Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    print("✅ Django настроен")
    
    from pwa.models import OrthodoxEvent, DailyOrthodoxInfo, FastingPeriod
    print("✅ Модели импортированы")
    
    # 1. Удаляем все данные из таблиц
    print("\n🗑️ Удаление данных из базы данных...")
    
    # Удаляем все события
    orthodox_count = OrthodoxEvent.objects.count()
    if orthodox_count > 0:
        OrthodoxEvent.objects.all().delete()
        print(f"   ✅ Удалено православных событий: {orthodox_count}")
    else:
        print(f"   ℹ️ Православных событий не найдено")
    
    # Удаляем ежедневную информацию
    daily_count = DailyOrthodoxInfo.objects.count()
    if daily_count > 0:
        DailyOrthodoxInfo.objects.all().delete()
        print(f"   ✅ Удалено записей ежедневной информации: {daily_count}")
    else:
        print(f"   ℹ️ Ежедневной информации не найдено")
    
    # Удаляем периоды постов
    fasting_count = FastingPeriod.objects.count()
    if fasting_count > 0:
        FastingPeriod.objects.all().delete()
        print(f"   ✅ Удалено периодов постов: {fasting_count}")
    else:
        print(f"   ℹ️ Периодов постов не найдено")
    
    print(f"\n🎉 База данных очищена от всех данных календаря!")
    
except Exception as e:
    print(f"❌ ОШИБКА при удалении данных: {e}")

print(f"\n📂 Файлы для ручного удаления:")
print(f"   🗑️ Шаблоны:")
print(f"      - templates/pwa/orthodox_calendar.html")
print(f"      - templates/pwa/orthodox_calendar_under_construction.html")
print(f"      - templates/pwa/daily_orthodox_calendar.html") 
print(f"      - templates/pwa/daily_orthodox_calendar_under_construction.html")
print(f"   🗑️ Скрипты:")
print(f"      - fix_july_*.py")
print(f"      - add_*_calendar.py")
print(f"      - orthodox_calendar*.py")

print(f"\n⚠️  ВНИМАНИЕ! После удаления файлов нужно:")
print(f"   1. Удалить URL записи из pwa/urls.py")
print(f"   2. Удалить views из pwa/views.py") 
print(f"   3. Создать миграцию: python manage.py makemigrations")
print(f"   4. Применить миграцию: python manage.py migrate")
print(f"   5. Убрать ссылки из меню")

input("\nНажмите Enter для завершения...")
