#!/usr/bin/env python
# create_test_data_simple.py - Быстрое создание тестовых данных

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from stories.models import Story
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType

def create_test_data():
    print("🧪 СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ")
    print("=" * 30)
    
    # Создаем тестового пользователя
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'first_name': 'Тест',
            'last_name': 'Пользователь',
            'email': 'test@example.com'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Создан пользователь: {user.username}")
    else:
        print(f"👤 Пользователь уже существует: {user.username}")
    
    # Получаем первый рассказ
    story = Story.objects.first()
    if not story:
        print("❌ Нет рассказов в базе! Сначала создайте рассказ.")
        return
    
    print(f"📖 Используем рассказ: {story.title}")
    
    # Создаем комментарии
    content_type = ContentType.objects.get_for_model(Story)
    
    comments_data = [
        "Очень душевный рассказ! Спасибо за видео. ❤️",
        "Прекрасная история, дети слушали с большим интересом.",
        "Благодарю за такой важный урок жизни! 🙏",
        "Замечательная подача материала, очень поучительно."
    ]
    
    created_count = 0
    for text in comments_data:
        comment, created = Comment.objects.get_or_create(
            content_type=content_type,
            object_id=story.id,
            author=user,
            text=text,
            defaults={'is_approved': True}
        )
        if created:
            created_count += 1
            print(f"✅ Создан комментарий: {text[:30]}...")
    
    # Создаем ответы
    if Comment.objects.filter(content_type=content_type, object_id=story.id).exists():
        parent = Comment.objects.filter(content_type=content_type, object_id=story.id).first()
        reply, created = Comment.objects.get_or_create(
            content_type=content_type,
            object_id=story.id,
            author=user,
            parent=parent,
            text="Полностью согласен! Очень трогательно.",
            defaults={'is_approved': True}
        )
        if created:
            created_count += 1
            print(f"✅ Создан ответ к комментарию")
    
    total_comments = Comment.objects.filter(content_type=content_type, object_id=story.id).count()
    print(f"\n🎉 Готово! Всего комментариев: {total_comments}")
    print(f"🔗 Тестовая ссылка: http://127.0.0.1:8000/stories/{story.slug}/")
    print(f"🔑 Логин: testuser, Пароль: testpass123")

if __name__ == "__main__":
    create_test_data()
