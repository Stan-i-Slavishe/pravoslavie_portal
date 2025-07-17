#!/usr/bin/env python
"""
🔍 Мониторинг памяти системы
"""
import psutil
import time

def check_memory_status():
    """Проверка состояния памяти"""
    print("💾 Статус памяти системы:")
    print("=" * 40)
    
    # Получаем информацию о памяти
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Физическая память
    total_gb = memory.total / (1024**3)
    used_gb = memory.used / (1024**3)
    free_gb = memory.available / (1024**3)
    
    print(f"📊 Физическая память:")
    print(f"  Всего: {total_gb:.1f} ГБ")
    print(f"  Используется: {used_gb:.1f} ГБ ({memory.percent:.1f}%)")
    print(f"  Доступно: {free_gb:.1f} ГБ")
    
    # Определяем статус
    if memory.percent < 50:
        status = "✅ ОТЛИЧНО"
        advice = "Система работает быстро"
    elif memory.percent < 70:
        status = "⚠️ НОРМАЛЬНО"
        advice = "Можно работать комфортно"
    elif memory.percent < 85:
        status = "🔄 ВНИМАНИЕ"
        advice = "Возможны небольшие тормоза"
    elif memory.percent < 95:
        status = "🐌 ПЛОХО"
        advice = "Сильные тормоза, нужно освободить память"
    else:
        status = "🚫 КРИТИЧНО"
        advice = "Система может зависнуть!"
    
    print(f"\n🎯 Статус: {status}")
    print(f"💡 Совет: {advice}")
    
    # Файл подкачки
    if swap.total > 0:
        swap_gb = swap.total / (1024**3)
        swap_used_gb = swap.used / (1024**3)
        print(f"\n💿 Файл подкачки:")
        print(f"  Всего: {swap_gb:.1f} ГБ")
        print(f"  Используется: {swap_used_gb:.1f} ГБ ({swap.percent:.1f}%)")
        
        if swap.percent > 10:
            print("  ⚠️ Система использует диск вместо RAM - это замедляет работу!")

def find_memory_hogs():
    """Поиск процессов, жрущих память"""
    print("\n🐽 Топ-5 процессов по использованию памяти:")
    print("-" * 50)
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            memory_mb = proc.info['memory_info'].rss / (1024**2)
            processes.append({
                'name': proc.info['name'],
                'pid': proc.info['pid'],
                'memory_mb': memory_mb
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Сортируем по памяти
    top_processes = sorted(processes, key=lambda x: x['memory_mb'], reverse=True)[:5]
    
    for i, proc in enumerate(top_processes, 1):
        print(f"{i}. {proc['name']}: {proc['memory_mb']:.1f} МБ (PID: {proc['pid']})")

def django_recommendations():
    """Рекомендации для Django"""
    memory = psutil.virtual_memory()
    
    print(f"\n🐍 Рекомендации для Django:")
    print("-" * 30)
    
    if memory.percent < 70:
        print("✅ Достаточно памяти для Django разработки")
        print("✅ Можно запускать DEBUG=True")
        print("✅ Можно использовать django-debug-toolbar")
    else:
        print("⚠️ Мало памяти, рекомендуется:")
        print("  • Использовать DEBUG=False")
        print("  • Отключить django-debug-toolbar")
        print("  • Использовать settings_performance.py")
        print("  • Закрыть лишние приложения")

if __name__ == "__main__":
    check_memory_status()
    find_memory_hogs()
    django_recommendations()
    
    print(f"\n🔄 Мониторинг в реальном времени...")
    try:
        while True:
            time.sleep(5)
            memory = psutil.virtual_memory()
            print(f"Память: {memory.percent:.1f}% | Доступно: {memory.available/(1024**3):.1f} ГБ", end='\r')
    except KeyboardInterrupt:
        print(f"\n\n✅ Мониторинг завершен")
