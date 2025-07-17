#!/usr/bin/env python
"""
🔍 Диагностика Django процессов
"""
import psutil
import sys
import os

def find_django_processes():
    """Поиск процессов Django"""
    print("🔍 Поиск процессов Django...")
    print("=" * 50)
    
    django_processes = []
    python_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_info', 'cpu_percent']):
        try:
            # Ищем Python процессы
            if 'python' in proc.info['name'].lower():
                python_processes.append(proc.info)
                
                # Ищем Django в командной строке
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if any(keyword in cmdline.lower() for keyword in ['django', 'manage.py', 'runserver']):
                    django_processes.append({
                        'pid': proc.info['pid'],
                        'cmdline': cmdline,
                        'memory_mb': proc.info['memory_info'].rss / 1024 / 1024,
                        'cpu_percent': proc.info['cpu_percent']
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    print(f"🐍 Найдено Python процессов: {len(python_processes)}")
    print(f"🌐 Найдено Django процессов: {len(django_processes)}")
    print()
    
    if django_processes:
        print("📊 Django процессы:")
        for proc in django_processes:
            print(f"  PID: {proc['pid']}")
            print(f"  Память: {proc['memory_mb']:.1f} MB")
            print(f"  ЦП: {proc['cpu_percent']:.1f}%")
            print(f"  Команда: {proc['cmdline'][:100]}...")
            print("-" * 40)
    else:
        print("✅ Django сервер не запущен")
    
    print("\n🔍 Все Python процессы:")
    for proc in python_processes:
        memory_mb = proc['memory_info'].rss / 1024 / 1024
        cmdline = ' '.join(proc['cmdline']) if proc['cmdline'] else 'N/A'
        print(f"  PID: {proc['pid']} | Память: {memory_mb:.1f}MB | {cmdline[:60]}...")

def check_ports():
    """Проверка занятых портов"""
    print("\n🌐 Проверка портов Django...")
    ports = [8000, 8080, 3000, 5000]
    
    for port in ports:
        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port == port:
                try:
                    proc = psutil.Process(conn.pid)
                    print(f"  Порт {port}: занят процессом {proc.name()} (PID: {conn.pid})")
                except:
                    print(f"  Порт {port}: занят неизвестным процессом")
                break
        else:
            print(f"  Порт {port}: свободен")

def system_stats():
    """Статистика системы"""
    print("\n💻 Статистика системы:")
    
    # ЦП
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"  ЦП: {cpu_percent}%")
    
    # Память
    memory = psutil.virtual_memory()
    print(f"  Память: {memory.percent}% ({memory.used // 1024 // 1024}MB / {memory.total // 1024 // 1024}MB)")
    
    # Диск
    disk = psutil.disk_usage('/')
    print(f"  Диск: {disk.percent}%")

if __name__ == "__main__":
    find_django_processes()
    check_ports()
    system_stats()
    
    input("\nНажмите Enter для выхода...")
