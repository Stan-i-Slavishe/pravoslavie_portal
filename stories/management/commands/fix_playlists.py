from django.core.management.base import BaseCommand
from stories.models import Playlist
from django.db import transaction


class Command(BaseCommand):
    help = 'Исправляет проблемы с плейлистами'

    def handle(self, *args, **options):
        self.stdout.write("🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С ПЛЕЙЛИСТАМИ")
        self.stdout.write("=" * 50)
        
        try:
            with transaction.atomic():
                # Ищем проблемный плейлист 'борода'
                problematic_playlists = Playlist.objects.filter(slug='борода')
                
                if problematic_playlists.exists():
                    self.stdout.write(f"🔍 Найдено плейлистов с slug='борода': {problematic_playlists.count()}")
                    
                    for playlist in problematic_playlists:
                        self.stdout.write(f"   - ID: {playlist.id}")
                        self.stdout.write(f"   - Title: '{playlist.title}'")
                        self.stdout.write(f"   - Creator: {playlist.creator.username}")
                        
                        # Исправляем slug
                        new_slug = f"playlist-{playlist.creator.username}-{playlist.id}"
                        playlist.slug = new_slug
                        playlist.save()
                        self.stdout.write(self.style.SUCCESS(f"   ✅ Изменен slug на: '{new_slug}'"))
                        
                else:
                    self.stdout.write(self.style.SUCCESS("✅ Проблемный плейлист 'борода' не найден"))
                
                # Проверяем все плейлисты
                self.stdout.write(f"\n📊 ТЕКУЩИЕ ПЛЕЙЛИСТЫ:")
                for playlist in Playlist.objects.all():
                    self.stdout.write(f"   - '{playlist.slug}' | '{playlist.title}' | {playlist.creator.username}")
                    
            self.stdout.write(self.style.SUCCESS("\n✅ ИСПРАВЛЕНИЯ ЗАВЕРШЕНЫ УСПЕШНО!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ ОШИБКА: {e}"))
