from django.core.management.base import BaseCommand
from stories.models import Playlist, PlaylistItem

class Command(BaseCommand):
    help = 'Исправляет порядок элементов во всех плейлистах'

    def handle(self, *args, **options):
        playlists = Playlist.objects.all()
        
        for playlist in playlists:
            self.stdout.write(f'Исправляем плейлист: {playlist.title}')
            
            # Получаем все элементы плейлиста, отсортированные по order
            items = PlaylistItem.objects.filter(playlist=playlist).order_by('order', 'id')
            
            # Переназначаем порядковые номера начиная с 1
            for index, item in enumerate(items, 1):
                if item.order != index:
                    item.order = index
                    item.save(update_fields=['order'])
                    self.stdout.write(f'  - Элемент {item.story.title}: order изменен на {index}')
        
        self.stdout.write(self.style.SUCCESS('Порядок элементов исправлен во всех плейлистах!'))
