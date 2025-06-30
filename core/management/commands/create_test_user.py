from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from stories.models import Story

User = get_user_model()

class Command(BaseCommand):
    help = 'Создает тестового пользователя для комментариев'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Создание тестовых данных для комментариев...")
        
        # Удаляем старого тестового пользователя если есть
        try:
            old_user = User.objects.get(username='testuser')
            old_user.delete()
            self.stdout.write("❌ Удален старый тестовый пользователь")
        except User.DoesNotExist:
            pass
        
        # Создаем правильного тестового пользователя
        try:
            user = User.objects.create_user(
                username='testuser',
                email='testuser@example.com',  # ✅ Правильный email
                password='password123',
                first_name='Тестовый',
                last_name='Пользователь'
            )
            self.stdout.write(f"✅ Создан тестовый пользователь: {user.username}")
            self.stdout.write(f"   Email: {user.email}")
            self.stdout.write(f"   Пароль: password123")
            
        except Exception as e:
            self.stdout.write(f"❌ Ошибка создания пользователя: {e}")
            return
        
        # Проверяем наличие рассказов
        stories_count = Story.objects.count()
        self.stdout.write(f"📚 Найдено рассказов в базе: {stories_count}")
        
        if stories_count == 0:
            self.stdout.write("⚠️  В базе нет рассказов для комментариев")
            self.stdout.write("   Создайте рассказы через админку или загрузите фикстуры")
        else:
            first_story = Story.objects.first()
            self.stdout.write(f"📖 Первый рассказ: {first_story.title}")
            self.stdout.write(f"   URL: http://127.0.0.1:8000/stories/{first_story.slug}/")
        
        self.stdout.write("")
        self.stdout.write("🎉 Тестовые данные готовы!")
        self.stdout.write("🚀 Теперь войдите в систему как:")
        self.stdout.write("   Логин: testuser")
        self.stdout.write("   Email: testuser@example.com")
        self.stdout.write("   Пароль: password123")
