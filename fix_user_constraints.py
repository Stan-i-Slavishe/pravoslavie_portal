#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Диагностика проблем с внешними ключами пользователей
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local_postgresql')
django.setup()

def check_user_references():
    """Проверяем все ссылки на пользователей"""
    
    from django.contrib.auth.models import User
    from django.db import connection
    
    print("ДИАГНОСТИКА СВЯЗЕЙ ПОЛЬЗОВАТЕЛЕЙ")
    print("=" * 40)
    
    # Получаем всех пользователей
    users = User.objects.all()
    print(f"Всего пользователей: {users.count()}")
    
    for user in users:
        print(f"\nПользователь: {user.username} (ID: {user.id})")
        
        # Проверяем связанные записи
        try:
            # Stories связи
            from stories.models import Story, StoryComment, StoryLike, Playlist
            
            stories_count = Story.objects.filter(category__isnull=True).count()  # Проверяем проблемные записи
            comments_count = StoryComment.objects.filter(user=user).count()
            likes_count = StoryLike.objects.filter(user=user).count()
            playlists_count = Playlist.objects.filter(creator=user).count()
            
            print(f"  - Комментарии: {comments_count}")
            print(f"  - Лайки: {likes_count}") 
            print(f"  - Плейлисты: {playlists_count}")
            
        except Exception as e:
            print(f"  - Ошибка проверки stories: {e}")
        
        # Проверяем другие связи
        try:
            from books.models import BookReview
            reviews_count = BookReview.objects.filter(user=user).count()
            print(f"  - Отзывы о книгах: {reviews_count}")
        except:
            pass

def check_orphaned_records():
    """Проверяем потерянные записи без пользователей"""
    
    from django.db import connection
    
    print("\nПОИСК ПОТЕРЯННЫХ ЗАПИСЕЙ")
    print("=" * 40)
    
    with connection.cursor() as cursor:
        # Ищем записи с несуществующими пользователями
        queries = [
            ("stories_storycomment", "user_id"),
            ("stories_storylike", "user_id"),  
            ("stories_playlist", "creator_id"),
            ("books_bookreview", "user_id"),
        ]
        
        for table, user_field in queries:
            try:
                cursor.execute(f"""
                    SELECT COUNT(*) FROM {table} 
                    WHERE {user_field} NOT IN (SELECT id FROM auth_user)
                """)
                orphaned_count = cursor.fetchone()[0]
                
                if orphaned_count > 0:
                    print(f"⚠ {table}: {orphaned_count} потерянных записей")
                else:
                    print(f"✓ {table}: все связи корректны")
                    
            except Exception as e:
                print(f"✗ {table}: ошибка проверки - {e}")

def fix_orphaned_records():
    """Исправляем потерянные записи"""
    
    from django.db import connection
    
    print("\nИСПРАВЛЕНИЕ ПОТЕРЯННЫХ ЗАПИСЕЙ")
    print("=" * 40)
    
    with connection.cursor() as cursor:
        # Удаляем записи с несуществующими пользователями
        fix_queries = [
            ("stories_storycomment", "user_id", "комментарии"),
            ("stories_storylike", "user_id", "лайки"),
            ("stories_playlist", "creator_id", "плейлисты"),
            ("books_bookreview", "user_id", "отзывы"),
        ]
        
        for table, user_field, description in fix_queries:
            try:
                cursor.execute(f"""
                    DELETE FROM {table} 
                    WHERE {user_field} NOT IN (SELECT id FROM auth_user)
                """)
                deleted_count = cursor.rowcount
                
                if deleted_count > 0:
                    print(f"🗑 Удалено {deleted_count} потерянных записей из {description}")
                else:
                    print(f"✓ {description}: исправления не требуются")
                    
            except Exception as e:
                print(f"✗ Ошибка исправления {description}: {e}")

if __name__ == "__main__":
    check_user_references()
    check_orphaned_records()
    
    print("\nХотите исправить потерянные записи? (y/n)")
    response = input().lower().strip()
    
    if response == 'y':
        fix_orphaned_records()
        print("\nПотерянные записи исправлены. Попробуйте снова открыть админку.")
    else:
        print("\nИсправления не применены.")
