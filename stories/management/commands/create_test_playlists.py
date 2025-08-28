from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stories.models import Story, Playlist, PlaylistItem
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Создает тестовые плейлисты с превьюшками для демонстрации'

    def handle(self, *args, **options):
        try:
            # Получаем или создаем тестового пользователя
            user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@example.com',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            
            if created:
                user.set_password('admin123')
                user.save()
                self.stdout.write(f'Создан пользователь: {user.username}')
            
            # Получаем существующие рассказы
            stories = Story.objects.filter(is_published=True)[:10]
            
            if not stories.exists():
                self.stdout.write(self.style.WARNING('Нет опубликованных рассказов для создания плейлистов'))
                return
            
            # Создаем тестовые плейлисты
            playlists_data = [
                {
                    'title': 'Посмотреть позже',
                    'description': 'Автоматически созданный плейлист для сохранения видео на потом',
                    'playlist_type': 'private',
                    'stories': stories[:3]
                },
                {
                    'title': 'Гармонь',
                    'description': 'Рассказы под аккомпанемент гармони',
                    'playlist_type': 'public',
                    'stories': stories[2:5]
                },
                {
                    'title': 'Кукриниксы',
                    'description': 'Веселые и поучительные истории',
                    'playlist_type': 'private',
                    'stories': stories[5:8]
                },
                {
                    'title': 'Любимые рассказы',
                    'description': 'Подборка самых трогательных историй',
                    'playlist_type': 'public',
                    'stories': stories[3:7]
                },
                {
                    'title': 'Детские истории',
                    'description': 'Рассказы для самых маленьких',
                    'playlist_type': 'public',
                    'stories': stories[1:4]
                },
                {
                    'title': 'Праздничные рассказы',
                    'description': 'Истории к православным праздникам',
                    'playlist_type': 'private',
                    'stories': stories[6:9]
                }
            ]
            
            created_count = 0
            
            for playlist_data in playlists_data:
                # Создаем слаг
                base_slug = slugify(playlist_data['title'], allow_unicode=True)
                if not base_slug:
                    base_slug = 'playlist'
                
                slug = base_slug
                counter = 1
                while Playlist.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                # Создаем плейлист
                playlist, created = Playlist.objects.get_or_create(
                    title=playlist_data['title'],
                    creator=user,
                    defaults={
                        'slug': slug,
                        'description': playlist_data['description'],
                        'playlist_type': playlist_data['playlist_type']
                    }
                )
                
                if created:
                    # Добавляем рассказы в плейлист
                    for order, story in enumerate(playlist_data['stories'], 1):
                        PlaylistItem.objects.create(
                            playlist=playlist,
                            story=story,
                            order=order
                        )
                    
                    created_count += 1
                    self.stdout.write(f'Создан плейлист: "{playlist.title}" с {len(playlist_data["stories"])} рассказами')
                else:
                    self.stdout.write(f'Плейлист уже существует: "{playlist.title}"')
            
            self.stdout.write(
                self.style.SUCCESS(f'Успешно создано {created_count} плейлистов!')
            )
            
            # Показываем статистику
            total_playlists = Playlist.objects.filter(creator=user).count()
            total_public = Playlist.objects.filter(creator=user, playlist_type='public').count()
            total_private = Playlist.objects.filter(creator=user, playlist_type='private').count()
            
            self.stdout.write(f'\n📊 Статистика плейлистов пользователя {user.username}:')
            self.stdout.write(f'   Всего плейлистов: {total_playlists}')
            self.stdout.write(f'   Публичных: {total_public}')
            self.stdout.write(f'   Приватных: {total_private}')
            
            self.stdout.write(f'\n🔗 Для просмотра перейдите на: http://127.0.0.1:8000/stories/playlists/')
            self.stdout.write(f'   Войдите как: admin / admin123')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании плейлистов: {e}')
            )
