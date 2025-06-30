#!/usr/bin/env python
"""
Скрипт для создания тестовых данных для терапевтических сказок
Запускать: python manage.py shell < create_fairy_tales_data.py
"""

from fairy_tales.models import (
    FairyTaleCategory, 
    FairyTaleTemplate, 
    AgeGroup, 
    TherapeuticGoal
)
from django.utils.text import slugify

print("🧚‍♀️ Создаем тестовые данные для терапевтических сказок...")

# Создаем категории
categories_data = [
    # Для детей (3-12 лет)
    {
        'name': 'Преодоление страхов',
        'description': 'Сказки помогающие детям справиться со страхами темноты, монстров, одиночества и других детских фобий',
        'age_group': AgeGroup.CHILD,
        'icon': 'shield-check',
        'color': '#e74c3c',
        'order': 1
    },
    {
        'name': 'Дружба и общение',
        'description': 'Истории о том, как найти друзей, решить конфликты и научиться общаться с другими детьми',
        'age_group': AgeGroup.CHILD,
        'icon': 'people',
        'color': '#3498db',
        'order': 2
    },
    {
        'name': 'Послушание и дисциплина',
        'description': 'Сказки о важности послушания родителям, соблюдения правил и самоконтроля',
        'age_group': AgeGroup.CHILD,
        'icon': 'hand-thumbs-up',
        'color': '#27ae60',
        'order': 3
    },
    {
        'name': 'Доброта и сострадание',
        'description': 'Истории воспитывающие доброту, отзывчивость и умение помогать другим',
        'age_group': AgeGroup.CHILD,
        'icon': 'heart',
        'color': '#e91e63',
        'order': 4
    },
    
    # Для подростков (13-17 лет)
    {
        'name': 'Самооценка и уверенность',
        'description': 'Истории помогающие подросткам обрести уверенность в себе и здоровую самооценку',
        'age_group': AgeGroup.TEEN,
        'icon': 'person-check',
        'color': '#9b59b6',
        'order': 1
    },
    {
        'name': 'Отношения и дружба',
        'description': 'Сказки о подростковых отношениях, первой любви и настоящей дружбе',
        'age_group': AgeGroup.TEEN,
        'icon': 'hearts',
        'color': '#f39c12',
        'order': 2
    },
    
    # Для взрослых (18+)
    {
        'name': 'Преодоление стресса',
        'description': 'Терапевтические истории для снятия стресса и восстановления внутреннего равновесия',
        'age_group': AgeGroup.ADULT,
        'icon': 'peace',
        'color': '#1abc9c',
        'order': 1
    },
    {
        'name': 'Семейные отношения',
        'description': 'Сказки о гармонии в семье, прощении и укреплении семейных связей',
        'age_group': AgeGroup.ADULT,
        'icon': 'house-heart',
        'color': '#34495e',
        'order': 2
    },
    
    # Семейные (все возрасты)
    {
        'name': 'Православные ценности',
        'description': 'Семейные сказки, рассказывающие о православной вере, традициях и духовности',
        'age_group': AgeGroup.FAMILY,
        'icon': 'brightness-high',
        'color': '#f1c40f',
        'order': 1
    },
    {
        'name': 'Благодарность и смирение',
        'description': 'Истории о важности благодарности Богу и людям, смирении и терпении',
        'age_group': AgeGroup.FAMILY,
        'icon': 'hands-clapping',
        'color': '#8e44ad',
        'order': 2
    }
]

# Создаем категории
categories = {}
for cat_data in categories_data:
    category, created = FairyTaleCategory.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'slug': slugify(cat_data['name'], allow_unicode=True),
            'description': cat_data['description'],
            'age_group': cat_data['age_group'],
            'icon': cat_data['icon'],
            'color': cat_data['color'],
            'order': cat_data['order'],
            'is_active': True
        }
    )
    categories[cat_data['name']] = category
    if created:
        print(f"✅ Создана категория: {category.name}")
    else:
        print(f"⏭️  Категория уже существует: {category.name}")

# Шаблоны сказок
templates_data = [
    # Детские сказки
    {
        'title': 'Храбрый {name} и Ночной Страж',
        'category': 'Преодоление страхов',
        'short_description': 'Персонализированная сказка о том, как ребенок преодолевает страх темноты с помощью доброго ангела-хранителя',
        'therapeutic_goals': [TherapeuticGoal.FEARS, TherapeuticGoal.CONFIDENCE, TherapeuticGoal.FAITH],
        'content_template': '''Жил-был {name}, {age}-летний {gender_suffix}. Каждый вечер, когда мама выключала свет, {name} начинал(-а) бояться темноты. 
        
Но однажды в комнате появился яркий, но мягкий свет, и {name} увидел(-а) прекрасного ангела в белоснежных одеждах.

"Не бойся, {name}," - сказал ангел добрым голосом. "Я твой Ночной Страж. Бог послал меня охранять твой сон. В темноте нет ничего страшного - это время, когда природа отдыхает, а ангелы особенно близко к людям."

{name} узнал(-а), что {child_interests}, и это поможет в путешествии по волшебному миру снов...

(Сказка продолжается, адаптируясь под конкретную проблему: {main_problem})''',
        'target_age_min': 3,
        'target_age_max': 8,
        'is_free': True,
        'base_price': 0,
        'has_audio_option': True,
        'audio_price': 1500,
        'has_illustration_option': True,
        'illustration_price': 3000,
        'author': 'Мария Светлая',
        'is_published': True,
        'featured': True
    },
    {
        'title': 'Как {name} нашел(-шла) настоящего друга',
        'category': 'Дружба и общение',
        'short_description': 'История о застенчивом ребенке, который учится дружить и быть открытым для общения',
        'therapeutic_goals': [TherapeuticGoal.RELATIONSHIPS, TherapeuticGoal.CONFIDENCE, TherapeuticGoal.KINDNESS],
        'content_template': '''В одном городе жил(-а) {name}, очень добрый(-ая) {age}-летний(-яя) {gender_suffix}. {name} очень любил(-а) {child_interests}, но был(-а) немного застенчив(-а) и не знал(-а), как подружиться с другими детьми.

Проблема в том, что {main_problem}. Но однажды...

(История о том, как через доброту и искренность герой находит настоящих друзей)''',
        'target_age_min': 4,
        'target_age_max': 10,
        'is_free': False,
        'base_price': 1200,
        'has_audio_option': True,
        'audio_price': 1500,
        'has_illustration_option': True,
        'illustration_price': 2500,
        'author': 'Елена Добрая',
        'is_published': True,
        'featured': False
    },
    {
        'title': 'Непослушный {name} и мудрый наставник',
        'category': 'Послушание и дисциплина',
        'short_description': 'Поучительная сказка о важности послушания и последствиях непослушания',
        'therapeutic_goals': [TherapeuticGoal.BEHAVIOR, TherapeuticGoal.PATIENCE, TherapeuticGoal.KINDNESS],
        'content_template': '''Жил(-а) {name}, {age} лет. Иногда {name} не хотел(-а) слушаться маму и папу, особенно когда {main_problem}.

Но в один удивительный день {name} встретил(-а) мудрого старца, который рассказал удивительную историю...

(Сказка показывает последствия непослушания и радость от правильных поступков)''',
        'target_age_min': 4,
        'target_age_max': 12,
        'is_free': False,
        'base_price': 1000,
        'has_audio_option': True,
        'audio_price': 1200,
        'has_illustration_option': False,
        'illustration_price': 0,
        'author': 'Отец Николай',
        'is_published': True,
        'featured': False
    },
    
    # Подростковые сказки
    {
        'title': 'Путь {name} к внутренней силе',
        'category': 'Самооценка и уверенность',
        'short_description': 'Вдохновляющая история для подростков о поиске себя и обретении уверенности',
        'therapeutic_goals': [TherapeuticGoal.CONFIDENCE, TherapeuticGoal.EMOTIONS, TherapeuticGoal.FAITH],
        'content_template': '''{name}, {age} лет, переживал(-а) трудное время. {main_problem} - эта ситуация сильно влияла на самооценку.

Но однажды {name} получил(-а) неожиданное письмо от бабушки, в котором была вложена старинная книга о святых подвижниках...

(История показывает, как через веру и самопознание подросток обретает внутреннюю силу)''',
        'target_age_min': 13,
        'target_age_max': 17,
        'is_free': False,
        'base_price': 2000,
        'has_audio_option': True,
        'audio_price': 2000,
        'has_illustration_option': True,
        'illustration_price': 4000,
        'author': 'Анна Мудрая',
        'is_published': True,
        'featured': True
    },
    
    # Взрослые сказки
    {
        'title': 'Тихая гавань для {name}',
        'category': 'Преодоление стресса',
        'short_description': 'Медитативная сказка для взрослых о поиске внутреннего покоя и преодолении стресса',
        'therapeutic_goals': [TherapeuticGoal.STRESS, TherapeuticGoal.EMOTIONS, TherapeuticGoal.FAITH, TherapeuticGoal.GRATITUDE],
        'content_template': '''Это история для {name}, который(-ая) переживает непростой период. {main_problem} - эта ситуация требует особого внимания и заботы о себе.

Представьте себя в тихом монастырском саду на рассвете. Здесь время течет по-особому...

(Медитативная история о поиске покоя через молитву и созерцание)''',
        'target_age_min': 18,
        'target_age_max': 99,
        'is_free': False,
        'base_price': 2500,
        'has_audio_option': True,
        'audio_price': 2500,
        'has_illustration_option': False,
        'illustration_price': 0,
        'author': 'Матушка Серафима',
        'is_published': True,
        'featured': False
    },
    
    # Семейные сказки
    {
        'title': 'Семья {name} и чудо благодарности',
        'category': 'Благодарность и смирение',
        'short_description': 'Семейная история о важности благодарности и совместной молитвы',
        'therapeutic_goals': [TherapeuticGoal.GRATITUDE, TherapeuticGoal.FAITH, TherapeuticGoal.RELATIONSHIPS, TherapeuticGoal.PATIENCE],
        'content_template': '''В одной православной семье жил(-а) {name} со своими родными. {family_situation}

Проблема заключалась в том, что {main_problem}. Но накануне большого церковного праздника произошло нечто удивительное...

(История о том, как семейная молитва и благодарность Богу помогают преодолеть трудности)''',
        'target_age_min': 5,
        'target_age_max': 99,
        'is_free': True,
        'base_price': 0,
        'has_audio_option': True,
        'audio_price': 1800,
        'has_illustration_option': True,
        'illustration_price': 3500,
        'author': 'Семья Светловых',
        'is_published': True,
        'featured': True
    }
]

# Создаем шаблоны сказок
for template_data in templates_data:
    category = categories.get(template_data['category'])
    if not category:
        print(f"❌ Категория '{template_data['category']}' не найдена для шаблона '{template_data['title']}'")
        continue
    
    template, created = FairyTaleTemplate.objects.get_or_create(
        title=template_data['title'],
        defaults={
            'slug': slugify(template_data['title'].replace('{name}', 'name'), allow_unicode=True),
            'category': category,
            'short_description': template_data['short_description'],
            'therapeutic_goals': template_data['therapeutic_goals'],
            'content_template': template_data['content_template'],
            'target_age_min': template_data['target_age_min'],
            'target_age_max': template_data['target_age_max'],
            'is_free': template_data['is_free'],
            'base_price': template_data['base_price'],
            'has_audio_option': template_data['has_audio_option'],
            'audio_price': template_data['audio_price'],
            'has_illustration_option': template_data['has_illustration_option'],
            'illustration_price': template_data['illustration_price'],
            'author': template_data['author'],
            'is_published': template_data['is_published'],
            'featured': template_data['featured']
        }
    )
    
    if created:
        print(f"✅ Создан шаблон сказки: {template.title}")
    else:
        print(f"⏭️  Шаблон уже существует: {template.title}")

print("\n🎉 Готово! Созданы:")
print(f"   📂 {FairyTaleCategory.objects.count()} категорий")
print(f"   📖 {FairyTaleTemplate.objects.count()} шаблонов сказок")
print(f"   ✨ {FairyTaleTemplate.objects.filter(featured=True).count()} рекомендуемых сказок")
print(f"   🆓 {FairyTaleTemplate.objects.filter(is_free=True).count()} бесплатных сказок")

print("\n🔗 Ссылки для проверки:")
print("   Каталог сказок: /fairy-tales/")
print("   Категории: /fairy-tales/categories/")
print("   Админка: /admin/fairy_tales/")
