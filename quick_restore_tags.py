#!/usr/bin/env python
"""
Быстрое восстановление тегов по названиям рассказов
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story
from core.models import Tag

# Словарь соответствий ключевых слов тегам
TAG_MAPPING = {
    'алкоголь': ['алкоголь', 'пить', 'выпивка', 'пьян'],
    'бабушка': ['бабушка', 'бабуля', 'старушка'],
    'бандиты': ['бандит', 'преступник', 'грабеж', 'воровство'],
    'внутренняя сила': ['сила', 'мужество', 'храбрость', 'стойкость'],
    'ВОВ': ['война', 'фронт', 'солдат', 'победа', 'военный'],
    'вразумление': ['вразумление', 'урок', 'наказание', 'поучение'],
    'врачебные истории': ['врач', 'доктор', 'больница', 'лечение', 'медицин'],
    'гонения': ['гонение', 'преследование', 'арест', 'тюрьма'],
    'дедушка': ['дедушка', 'дед', 'старик'],
    'дети': ['дети', 'ребенок', 'малыш', 'детский', 'девочка', 'мальчик'],
    'доброе слово': ['слово', 'совет', 'поддержка', 'утешение'],
    'дочь': ['дочь', 'дочка'],
    'животные': ['собака', 'кот', 'животное', 'зверь', 'кошка', 'пес'],
    'жертвенность': ['жертва', 'самопожертвование', 'отдать'],
    'за пределами логики': ['чудо', 'необъяснимое', 'таинственн'],
    'испытания': ['испытание', 'трудность', 'беда', 'несчастье'],
    'истории из жизни': ['жизнь', 'быт', 'повседневность', 'житейск'],
    'исцеление': ['исцеление', 'излечение', 'здоровье', 'выздоровление'],
    'кротость': ['кротость', 'смирение', 'терпение', 'тихий'],
    'мама': ['мама', 'мать', 'мамочка', 'матушка'],
    'молитва': ['молитва', 'молиться', 'молебен'],
    'моя половинка': ['жена', 'муж', 'супруг', 'брак', 'семейн'],
    'Папа': ['папа', 'отец', 'батя', 'батюшка'],
    'покаяние': ['покаяние', 'исповедь', 'грех', 'раскаяние'],
    'простая радость': ['радость', 'счастье', 'веселье', 'праздник'],
    'семья': ['семья', 'родители', 'дом', 'домашн'],
    'сильная личность': ['личность', 'характер', 'воля', 'сильный'],
    'смирение': ['смирение', 'покорность', 'послушание'],
    'сострадание': ['сострадание', 'милосердие', 'жалость', 'помощь'],
    'сын': ['сын', 'сынок'],
    'христианская любовь': ['любовь', 'христианский', 'церковн'],
    'чудеса': ['чудо', 'чудесный', 'необычное', 'удивительн'],
    'школа': ['школа', 'учитель', 'ученик', 'урок', 'образование']
}

def restore_tags():
    """Восстанавливает теги для всех рассказов"""
    print("🚀 Быстрое восстановление тегов...")
    
    # Статистика
    restored_count = 0
    total_tags_assigned = 0
    
    # Получаем все рассказы
    stories = Story.objects.all()
    print(f"📚 Обрабатываем {stories.count()} рассказов...")
    
    for story in stories:
        # Очищаем существующие теги
        story.tags.clear()
        
        # Объединяем название и описание
        text_content = f"{story.title} {story.description}".lower()
        
        # Ищем подходящие теги
        assigned_tags = []
        for tag_name, keywords in TAG_MAPPING.items():
            try:
                tag = Tag.objects.get(name=tag_name)
                # Проверяем, есть ли ключевые слова в тексте
                if any(keyword in text_content for keyword in keywords):
                    story.tags.add(tag)
                    assigned_tags.append(tag_name)
                    total_tags_assigned += 1
            except Tag.DoesNotExist:
                print(f"⚠️ Тег '{tag_name}' не найден в базе")
                continue
        
        if assigned_tags:
            restored_count += 1
            print(f"✅ '{story.title}' → {len(assigned_tags)} тегов: {', '.join(assigned_tags[:3])}{'...' if len(assigned_tags) > 3 else ''}")
    
    print(f"\n📊 РЕЗУЛЬТАТ:")
    print(f"✅ Рассказов с восстановленными тегами: {restored_count}")
    print(f"🏷️ Всего назначено тегов: {total_tags_assigned}")
    print(f"📈 Среднее количество тегов на рассказ: {total_tags_assigned/restored_count:.1f}" if restored_count > 0 else "")

def check_missing_tags():
    """Проверяет, какие теги отсутствуют в базе"""
    print("\n🔍 Проверка отсутствующих тегов...")
    
    missing_tags = []
    for tag_name in TAG_MAPPING.keys():
        if not Tag.objects.filter(name=tag_name).exists():
            missing_tags.append(tag_name)
    
    if missing_tags:
        print(f"❌ Отсутствуют теги ({len(missing_tags)}):")
        for tag in missing_tags:
            print(f"  - {tag}")
        
        create_missing = input("\nСоздать отсутствующие теги? (y/n): ").lower()
        if create_missing == 'y':
            created_count = 0
            for tag_name in missing_tags:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'slug': tag_name.lower().replace(' ', '-')}
                )
                if created:
                    created_count += 1
                    print(f"✅ Создан тег: {tag_name}")
            print(f"📊 Создано тегов: {created_count}")
    else:
        print("✅ Все необходимые теги присутствуют в базе")

def show_statistics():
    """Показывает статистику тегов"""
    print("\n📊 СТАТИСТИКА ТЕГОВ:")
    
    total_stories = Story.objects.count()
    stories_with_tags = Story.objects.filter(tags__isnull=False).distinct().count()
    stories_without_tags = total_stories - stories_with_tags
    
    print(f"📚 Всего рассказов: {total_stories}")
    print(f"✅ С тегами: {stories_with_tags}")
    print(f"❌ Без тегов: {stories_without_tags}")
    
    if stories_without_tags > 0:
        print(f"\n📝 Рассказы без тегов:")
        for story in Story.objects.filter(tags__isnull=True)[:10]:
            print(f"  - {story.title}")

def main():
    """Главная функция"""
    print("🏷️ БЫСТРОЕ ВОССТАНОВЛЕНИЕ ТЕГОВ")
    print("=" * 40)
    
    # Показываем текущую статистику
    show_statistics()
    
    # Проверяем отсутствующие теги
    check_missing_tags()
    
    # Запрашиваем подтверждение
    print("\n" + "=" * 40)
    confirm = input("🚀 Начать восстановление тегов? (y/n): ").lower()
    
    if confirm == 'y':
        restore_tags()
        # Показываем финальную статистику
        show_statistics()
        print("\n✅ Восстановление завершено!")
    else:
        print("❌ Восстановление отменено")

if __name__ == "__main__":
    main()
