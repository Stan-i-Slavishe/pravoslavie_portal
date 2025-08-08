"""
Команды для выполнения в Django shell
python manage.py shell
"""

from core.models import Tag
from stories.models import Story

# 1. Проверяем существующие теги
print("Все теги:")
for tag in Tag.objects.all():
    print(f"- {tag.name} (slug: {tag.slug})")

# 2. Создаем тег "дочь" если его нет
if not Tag.objects.filter(slug='doch').exists():
    doch_tag = Tag.objects.create(
        name='дочь',
        slug='doch',
        description='Материалы о воспитании дочерей и отношениях с ними',
        color='#FF6B9D',
        is_active=True
    )
    print(f"Создан тег: {doch_tag.name}")

# 3. Создаем другие базовые теги
basic_tags = [
    {'name': 'сын', 'slug': 'syn', 'description': 'Материалы о воспитании сыновей', 'color': '#2196F3'},
    {'name': 'семья', 'slug': 'semya', 'description': 'Материалы о семейных ценностях', 'color': '#4CAF50'},
    {'name': 'вера', 'slug': 'vera', 'description': 'Материалы о вере и духовности', 'color': '#9C27B0'},
    {'name': 'любовь', 'slug': 'lyubov', 'description': 'Материалы о любви', 'color': '#E91E63'},
]

for tag_data in basic_tags:
    if not Tag.objects.filter(slug=tag_data['slug']).exists():
        tag = Tag.objects.create(**tag_data, is_active=True)
        print(f"Создан тег: {tag.name}")

# 4. Добавляем теги к рассказам
if Story.objects.exists():
    # Получаем первые несколько рассказов и добавляем им теги
    stories = Story.objects.all()[:5]
    doch_tag = Tag.objects.get(slug='doch')
    semya_tag = Tag.objects.get(slug='semya')
    
    for i, story in enumerate(stories):
        if i % 2 == 0:
            story.tags.add(doch_tag)
        else:
            story.tags.add(semya_tag)
        print(f"К рассказу '{story.title}' добавлены теги")

print("✅ Теги созданы и настроены!")
