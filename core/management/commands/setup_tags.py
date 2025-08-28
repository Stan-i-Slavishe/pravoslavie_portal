from django.core.management.base import BaseCommand
from core.models import Tag
from stories.models import Story


class Command(BaseCommand):
    help = 'Создает базовые теги и исправляет систему тегов'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Исправление системы тегов...")
        
        # Создаем базовые теги
        basic_tags = [
            {
                'name': 'дочь', 
                'slug': 'doch', 
                'description': 'Материалы о воспитании дочерей и отношениях с ними',
                'color': '#FF6B9D'
            },
            {
                'name': 'сын', 
                'slug': 'syn', 
                'description': 'Материалы о воспитании сыновей',
                'color': '#2196F3'
            },
            {
                'name': 'семья', 
                'slug': 'semya', 
                'description': 'Материалы о семейных ценностях',
                'color': '#4CAF50'
            },
            {
                'name': 'вера', 
                'slug': 'vera', 
                'description': 'Материалы о вере и духовности',
                'color': '#9C27B0'
            },
            {
                'name': 'любовь', 
                'slug': 'lyubov', 
                'description': 'Материалы о любви',
                'color': '#E91E63'
            },
            {
                'name': 'отец', 
                'slug': 'otets', 
                'description': 'Материалы об отцовстве',
                'color': '#795548'
            }
        ]
        
        created_count = 0
        for tag_data in basic_tags:
            tag, created = Tag.objects.get_or_create(
                slug=tag_data['slug'],
                defaults={
                    'name': tag_data['name'],
                    'description': tag_data['description'],
                    'color': tag_data['color'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Создан тег: {tag.name} (slug: {tag.slug})")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ Тег уже существует: {tag.name}")
                )
        
        # Добавляем теги к рассказам, если они есть
        stories_count = Story.objects.count()
        if stories_count > 0:
            self.stdout.write(f"📚 Найдено {stories_count} рассказов")
            
            # Получаем созданные теги
            doch_tag = Tag.objects.get(slug='doch')
            semya_tag = Tag.objects.get(slug='semya')
            vera_tag = Tag.objects.get(slug='vera')
            
            # Добавляем теги к рассказам без тегов
            stories_without_tags = Story.objects.filter(tags__isnull=True)[:10]
            
            for i, story in enumerate(stories_without_tags):
                # Распределяем теги по рассказам
                if i % 3 == 0:
                    story.tags.add(doch_tag)
                    self.stdout.write(f"🏷️ К '{story.title}' добавлен тег 'дочь'")
                elif i % 3 == 1:
                    story.tags.add(semya_tag)
                    self.stdout.write(f"🏷️ К '{story.title}' добавлен тег 'семья'")
                else:
                    story.tags.add(vera_tag)
                    self.stdout.write(f"🏷️ К '{story.title}' добавлен тег 'вера'")
        
        # Статистика
        total_tags = Tag.objects.count()
        active_tags = Tag.objects.filter(is_active=True).count()
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!"))
        self.stdout.write(f"📊 Всего тегов: {total_tags}")
        self.stdout.write(f"📊 Активных тегов: {active_tags}")
        self.stdout.write(f"📊 Создано новых тегов: {created_count}")
        self.stdout.write("\n🧪 Теперь можете протестировать:")
        self.stdout.write("   http://127.0.0.1:8000/tag/doch/")
        self.stdout.write("   http://127.0.0.1:8000/tag/vera/")
        self.stdout.write("   http://127.0.0.1:8000/tag/semya/")
