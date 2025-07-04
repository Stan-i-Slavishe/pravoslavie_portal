python manage.py shell << 'EOF'
from stories.models import Playlist
print("=== ПРОВЕРКА ПЛЕЙЛИСТОВ ===")
playlists = Playlist.objects.all()
print(f"Всего плейлистов: {playlists.count()}")
for p in playlists:
    print(f"ID: {p.id}, Slug: '{p.slug}', Title: '{p.title}', Creator: {p.creator.username}")
problem = Playlist.objects.filter(slug='борода').first()
if problem:
    print(f"🔍 Найден 'борода': Creator={problem.creator.username}")
else:
    print("✅ 'борода' не найден")
EOF