@echo off
cd /d "E:\pravoslavie_portal"
call .venv\Scripts\activate.bat

echo Fixing playlist issue...

python -c "import os,django;os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings');django.setup();from stories.models import Playlist;[setattr(p,'slug',f'playlist-fixed-{p.id}') or p.save() or print(f'Fixed: {p.slug}') for p in Playlist.objects.filter(slug__contains='борода')];print('Done!')"

echo.
echo Fixed! Reload your browser page.
pause
