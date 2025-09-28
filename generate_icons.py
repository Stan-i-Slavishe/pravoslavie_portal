"""
Скрипт для генерации недостающих иконок PWA
"""
from PIL import Image
import os

# Путь к иконкам
ICONS_DIR = 'static/icons'

# Размеры, которые нужно создать
SIZES = [96, 128, 144, 384]

def resize_icon(source_path, target_size, output_path):
    """Изменяет размер иконки с сохранением качества"""
    img = Image.open(source_path)
    img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    img.save(output_path, 'PNG', optimize=True)
    print(f"✅ Created: {output_path}")

def create_badge(source_path, output_path):
    """Создает badge-иконку (монохромная, упрощенная)"""
    # Открываем оригинал
    img = Image.open(source_path)
    
    # Уменьшаем до 72x72
    img = img.resize((72, 72), Image.Resampling.LANCZOS)
    
    # Конвертируем в RGBA если нужно
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Сохраняем
    img.save(output_path, 'PNG', optimize=True)
    print(f"✅ Created badge: {output_path}")

def main():
    print("🎨 Генерация иконок PWA...")
    
    source_icon = os.path.join(ICONS_DIR, 'icon-512x512.png')
    
    if not os.path.exists(source_icon):
        print(f"❌ Исходная иконка не найдена: {source_icon}")
        return
    
    # Создаем промежуточные размеры
    for size in SIZES:
        output_path = os.path.join(ICONS_DIR, f'icon-{size}x{size}.png')
        if not os.path.exists(output_path):
            resize_icon(source_icon, size, output_path)
        else:
            print(f"⏭️  Пропуск (уже существует): {output_path}")
    
    # Создаем badge
    badge_path = os.path.join(ICONS_DIR, 'badge-72x72.png')
    if not os.path.exists(badge_path):
        create_badge(source_icon, badge_path)
    else:
        print(f"⏭️  Пропуск (уже существует): {badge_path}")
    
    print("✨ Генерация завершена!")

if __name__ == '__main__':
    main()
