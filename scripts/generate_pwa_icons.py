#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Генератор иконок PWA для Православного портала
"""

from PIL import Image
import os
import sys

def main():
    print("🎨 Генерация иконок PWA...")
    
    # Путь к иконкам
    icons_dir = 'static/icons'
    
    # Проверяем существование директории
    if not os.path.exists(icons_dir):
        print(f"❌ Директория не найдена: {icons_dir}")
        sys.exit(1)
    
    source_icon = os.path.join(icons_dir, 'icon-512x512.png')
    
    if not os.path.exists(source_icon):
        print(f"❌ Исходная иконка не найдена: {source_icon}")
        sys.exit(1)
    
    # Открываем исходную иконку
    img = Image.open(source_icon)
    print(f"✅ Загружена исходная иконка: {source_icon}")
    print(f"   Размер: {img.size}, Режим: {img.mode}")
    
    # Размеры для генерации
    sizes = [96, 128, 144, 384]
    
    # Создаем промежуточные размеры
    for size in sizes:
        output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        
        if os.path.exists(output_path):
            print(f"⏭️  Пропуск (уже существует): icon-{size}x{size}.png")
            continue
        
        # Изменяем размер
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(output_path, 'PNG', optimize=True)
        print(f"✅ Создан: icon-{size}x{size}.png")
    
    # Создаем badge (монохромная версия 72x72)
    badge_path = os.path.join(icons_dir, 'badge-72x72.png')
    
    if os.path.exists(badge_path):
        print(f"⏭️  Пропуск (уже существует): badge-72x72.png")
    else:
        # Уменьшаем до 72x72
        badge = img.resize((72, 72), Image.Resampling.LANCZOS)
        
        # Конвертируем в RGBA если нужно
        if badge.mode != 'RGBA':
            badge = badge.convert('RGBA')
        
        badge.save(badge_path, 'PNG', optimize=True)
        print(f"✅ Создан badge: badge-72x72.png")
    
    print("\n✨ Генерация иконок завершена успешно!")
    print("\n📋 Созданные файлы:")
    for size in sizes:
        path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        if os.path.exists(path):
            print(f"   ✓ icon-{size}x{size}.png")
    
    if os.path.exists(badge_path):
        print(f"   ✓ badge-72x72.png")

if __name__ == '__main__':
    main()
