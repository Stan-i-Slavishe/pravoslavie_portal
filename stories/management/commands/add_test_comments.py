from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stories.models import Story, StoryComment


class Command(BaseCommand):
    help = 'Добавляет тестовые комментарии к рассказам'
    
    def handle(self, *args, **options):
        self.stdout.write('🔧 Создание тестовых комментариев...')
        
        # Получаем пользователя admin или создаем
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            try:
                admin_user = User.objects.get(is_superuser=True)
            except User.DoesNotExist:
                admin_user = User.objects.create_user(
                    username='admin',
                    email='admin@example.com',
                    password='admin123',
                    is_superuser=True,
                    is_staff=True
                )
                self.stdout.write(f'✅ Создан пользователь admin')
        
        # Добавляем комментарии к рассказам
        stories = Story.objects.all()
        
        for story in stories:
            # Проверяем, есть ли уже комментарии
            existing_comments = story.comments.count()
            
            if existing_comments == 0:
                # Добавляем тестовые комментарии
                comments_to_add = [
                    f"Очень трогательный рассказ! Спасибо за такой контент.",
                    f"Благодарю за эту историю. Очень поучительно.",
                    f"Слушал с семьей, всем понравилось!",
                ]
                
                for i, comment_text in enumerate(comments_to_add):
                    StoryComment.objects.create(
                        story=story,
                        user=admin_user,
                        text=comment_text,
                        is_approved=True
                    )
                
                self.stdout.write(f'✅ Добавлено {len(comments_to_add)} комментариев к "{story.title}"')
            else:
                self.stdout.write(f'ℹ️ У рассказа "{story.title}" уже есть {existing_comments} комментариев')
        
        # Показываем статистику
        total_stories = stories.count()
        total_comments = StoryComment.objects.count()
        
        self.stdout.write('📊 Статистика:')
        self.stdout.write(f'   📖 Рассказов: {total_stories}')
        self.stdout.write(f'   💬 Комментариев: {total_comments}')
        
        self.stdout.write(self.style.SUCCESS('🎉 Тестовые комментарии готовы!'))
