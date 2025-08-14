#!/usr/bin/env python
"""
Скрипт для добавления тестовых терапевтических сказок
Запуск: python add_test_fairy_tales.py
"""

import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from fairy_tales.models import FairyTaleCategory, FairyTaleTemplate, TherapeuticGoal, AgeGroup

def create_test_data():
    """Создает тестовые данные для сказок"""
    
    print("🎭 Создание тестовых терапевтических сказок...")
    
    # 1. Создаем категории
    categories_data = [
        {
            'name': 'Преодоление страхов',
            'description': 'Сказки для помощи детям в преодолении различных страхов',
            'age_group': AgeGroup.CHILD,
            'icon': 'shield-check',
            'color': '#e74c3c',
            'order': 1
        },
        {
            'name': 'Развитие уверенности',
            'description': 'Истории для повышения самооценки и уверенности в себе',
            'age_group': AgeGroup.CHILD,
            'icon': 'star-fill',
            'color': '#f39c12',
            'order': 2
        },
        {
            'name': 'Семейные отношения',
            'description': 'Сказки о взаимоотношениях в семье',
            'age_group': AgeGroup.FAMILY,
            'icon': 'house-heart',
            'color': '#27ae60',
            'order': 3
        },
        {
            'name': 'Духовные ценности',
            'description': 'Православные сказки о вере, добре и милосердии',
            'age_group': AgeGroup.FAMILY,
            'icon': 'church',
            'color': '#3498db',
            'order': 4
        },
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = FairyTaleCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories[cat_data['name']] = category
        if created:
            print(f"✅ Создана категория: {category.name}")
        else:
            print(f"📂 Категория уже существует: {category.name}")
    
    # 2. Создаем сказки
    tales_data = [
        {
            'title': 'Маленький храбрец и тёмная комната',
            'category': categories['Преодоление страхов'],
            'short_description': 'История о мальчике, который научился не бояться темноты с помощью ангела-хранителя',
            'therapeutic_goals': [TherapeuticGoal.FEARS, TherapeuticGoal.CONFIDENCE, TherapeuticGoal.FAITH],
            'content_template': '''Жил-был маленький {name}, которому было {age} лет. Он очень боялся темноты и не мог засыпать без света. 
            
Каждый вечер {name} просил маму оставить свет в коридоре, потому что в темноте ему виделись страшные тени и слышались странные звуки.

Однажды ночью к {name} пришёл его ангел-хранитель. "Не бойся, {name}, - сказал ангел. - Бог всегда с тобой, даже в самой тёмной комнате."

Ангел показал {name}, что тёмная комната наполнена Божьей любовью и защитой. Тени оказались просто игрой света, а звуки - обычными домашними шумами.

С тех пор {name} не боится темноты, ведь он знает, что Бог всегда рядом и защищает его.''',
            'target_age_min': 3,
            'target_age_max': 8,
            'is_free': True,
            'base_price': 0,
            'has_audio_option': True,
            'audio_price': 300,
            'is_published': True,
            'featured': True,
        },
        {
            'title': 'Звёздочка, которая не светила',
            'category': categories['Развитие уверенности'],
            'short_description': 'Сказка о маленькой звёздочке, которая нашла свой особенный свет',
            'therapeutic_goals': [TherapeuticGoal.CONFIDENCE, TherapeuticGoal.PATIENCE],
            'content_template': '''На небе жила маленькая звёздочка по имени {name}. Она очень расстраивалась, потому что светила не так ярко, как другие звёзды.

{name} думала: "Я самая тусклая звёздочка на всём небе. Никто меня не замечает."

Но однажды на земле заблудился маленький ребёнок. Большие яркие звёзды светили так сильно, что слепили глаза, а вот нежный свет {name} помог ребёнку найти дорогу домой.

"Спасибо тебе, добрая звёздочка!" - сказал ребёнок. 

Тогда {name} поняла, что каждый особенный по-своему, и её мягкий свет тоже очень важен.''',
            'target_age_min': 4,
            'target_age_max': 10,
            'is_free': True,
            'base_price': 0,
            'has_audio_option': True,
            'audio_price': 300,
            'has_illustration_option': True,
            'illustration_price': 500,
            'is_published': True,
            'featured': True,
        },
        {
            'title': 'Семья медвежат и урок прощения',
            'category': categories['Семейные отношения'],
            'short_description': 'История о том, как важно прощать и просить прощения в семье',
            'therapeutic_goals': [TherapeuticGoal.FORGIVENESS, TherapeuticGoal.RELATIONSHIPS, TherapeuticGoal.KINDNESS],
            'content_template': '''В лесу жила семья медвежат. Старший медвежонок {name} часто ссорился со своей младшей сестрёнкой.

Однажды {name} сломал любимую игрушку сестрички и не хотел просить прощения. Он думал: "Это она виновата, что оставила игрушку не на месте!"

Мама-медведица рассказала {name} притчу о том, как Иисус учил прощать семьдесят раз семь раз. "Прощение - это не слабость, а сила, - сказала мама. - Оно лечит сердца и укрепляет семью."

{name} понял свою ошибку, попросил прощения у сестрички и даже починил её игрушку. С тех пор в их семье стало ещё больше любви и понимания.''',
            'target_age_min': 5,
            'target_age_max': 12,
            'is_free': False,
            'base_price': 500,
            'has_audio_option': True,
            'audio_price': 300,
            'has_illustration_option': True,
            'illustration_price': 700,
            'is_published': True,
        },
        {
            'title': 'Чудесный колокольчик святого Николая',
            'category': categories['Духовные ценности'],
            'short_description': 'Рождественская сказка о вере, надежде и чудесах',
            'therapeutic_goals': [TherapeuticGoal.FAITH, TherapeuticGoal.GRATITUDE, TherapeuticGoal.KINDNESS],
            'content_template': '''Перед Рождеством в маленькой деревушке жил мальчик {name}. Его семья была очень бедной, и на праздник не было денег даже на самые простые подарки.

{name} очень грустил, но мама сказала ему: "Самый лучший подарок - это наша вера и любовь друг к другу."

В рождественскую ночь {name} услышал звон колокольчика. Это был святой Николай! Он подарил {name} не золото и серебро, а нечто гораздо более ценное - понимание того, что истинное богатство в добрых делах.

{name} начал помогать соседям, делиться тем малым, что у него было. И вскоре вся деревня наполнилась радостью и взаимопомощью.

Так {name} понял, что настоящие чудеса происходят тогда, когда мы сами становимся чудом для других.''',
            'target_age_min': 6,
            'target_age_max': 14,
            'is_free': False,
            'base_price': 700,
            'has_audio_option': True,
            'audio_price': 400,
            'has_illustration_option': True,
            'illustration_price': 800,
            'is_published': True,
            'featured': True,
        },
        {
            'title': 'Грустная тучка и солнечный зайчик',
            'category': categories['Преодоление страхов'],
            'short_description': 'Сказка о том, как справиться с грустью и найти радость в жизни',
            'therapeutic_goals': [TherapeuticGoal.EMOTIONS, TherapeuticGoal.STRESS, TherapeuticGoal.PATIENCE],
            'content_template': '''Высоко в небе жила тучка по имени {name}. Она всегда была грустной и плакала дождиком.

"Почему ты всегда грустишь?" - спросил у неё солнечный зайчик.

"Я думаю только о плохом, - ответила {name}. - О том, что может случиться что-то страшное."

Солнечный зайчик научил {name} особой молитве: "Господи, помоги мне видеть красоту в каждом дне."

Постепенно {name} научилась замечать хорошее: как её дождик помогает расти цветам, как радуются птички после дождя, как красиво блестят капельки на листьях.

Теперь {name} плачет только тогда, когда это действительно нужно природе, а остальное время радуется жизни.''',
            'target_age_min': 4,
            'target_age_max': 9,
            'is_free': True,
            'base_price': 0,
            'has_audio_option': True,
            'audio_price': 300,
            'is_published': True,
        },
    ]
    
    for tale_data in tales_data:
        tale, created = FairyTaleTemplate.objects.get_or_create(
            title=tale_data['title'],
            defaults=tale_data
        )
        
        if created:
            print(f"✅ Создана сказка: {tale.title}")
        else:
            print(f"📖 Сказка уже существует: {tale.title}")
    
    print(f"\n🎉 Готово! Создано:")
    print(f"   📂 Категорий: {FairyTaleCategory.objects.count()}")
    print(f"   📖 Сказок: {FairyTaleTemplate.objects.count()}")
    print(f"   🆓 Бесплатных сказок: {FairyTaleTemplate.objects.filter(is_free=True).count()}")
    print(f"   💰 Платных сказок: {FairyTaleTemplate.objects.filter(is_free=False).count()}")
    print(f"\n🌟 Все сказки доступны по адресу: /fairy-tales/")

if __name__ == '__main__':
    create_test_data()
