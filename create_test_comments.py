import os
import sys
import django

# Добавляем путь к проекту
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализируем Django
django.setup()

from django.contrib.auth.models import User
from stories.models import Story, StoryComment, CommentReaction
from django.utils import timezone

def create_test_comments():
    """Создает тестовые комментарии для демонстрации"""
    
    print("🎬 Создание тестовых комментариев...")
    
    # Получаем первый рассказ
    try:
        story = Story.objects.first()
        if not story:
            print("❌ Нет рассказов для создания комментариев")
            return
            
        print(f"📝 Добавляем комментарии к рассказу: {story.title}")
        
        # Получаем или создаем тестового пользователя
        user1, created = User.objects.get_or_create(
            username='testuser1',
            defaults={
                'first_name': 'Алексей',
                'last_name': 'Петров',
                'email': 'test1@example.com'
            }
        )
        
        user2, created = User.objects.get_or_create(
            username='testuser2', 
            defaults={
                'first_name': 'Мария',
                'last_name': 'Сидорова',
                'email': 'test2@example.com'
            }
        )
        
        # Создаем основные комментарии
        comment1 = StoryComment.objects.create(
            story=story,
            user=user1,
            text="Прекрасный рассказ! Очень трогательно и поучительно. Спасибо за такой замечательный контент!",
            is_approved=True
        )
        
        comment2 = StoryComment.objects.create(
            story=story,
            user=user2,
            text="Смотрела с детьми, им очень понравилось. Будем ждать новых рассказов!",
            is_approved=True
        )
        
        comment3 = StoryComment.objects.create(
            story=story,
            user=user1,
            text="Такие истории нужно показывать в школах. Очень важные жизненные уроки.",
            is_approved=True
        )
        
        # Создаем ответы на комментарии
        reply1 = StoryComment.objects.create(
            story=story,
            user=user2,
            text="Полностью согласна! Это действительно важно для воспитания детей.",
            parent=comment1,
            is_approved=True
        )
        
        reply2 = StoryComment.objects.create(
            story=story,
            user=user1,
            text="Мария, а сколько лет вашим детям? Интересно знать возрастную аудиторию.",
            parent=comment2,
            is_approved=True
        )
        
        # Добавляем лайки к комментариям
        CommentReaction.objects.create(
            comment=comment1,
            user=user2,
            reaction_type='like'
        )
        
        CommentReaction.objects.create(
            comment=comment2,
            user=user1,
            reaction_type='like'
        )
        
        CommentReaction.objects.create(
            comment=reply1,
            user=user1,
            reaction_type='like'
        )
        
        print(f"✅ Создано {StoryComment.objects.filter(story=story).count()} комментариев")
        print(f"👍 Создано {CommentReaction.objects.filter(comment__story=story).count()} реакций")
        
    except Exception as e:
        print(f"❌ Ошибка при создании комментариев: {e}")

if __name__ == "__main__":
    create_test_comments()
    print("\n🎉 Готово! Тестовые комментарии созданы.")
