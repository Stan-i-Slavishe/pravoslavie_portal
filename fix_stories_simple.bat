@echo off
echo Starting story fix...

python manage.py shell -c "
from stories.models import Story
import re

def extract_youtube_id(url):
    if not url:
        return None
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
        r'youtube\.com/v/([^&\n?#]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

print('Fixing story...')
try:
    story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
    print(f'Found: {story.title}')
    
    if story.youtube_url and not story.youtube_embed_id:
        youtube_id = extract_youtube_id(story.youtube_url)
        if youtube_id:
            story.youtube_embed_id = youtube_id
            story.save(update_fields=['youtube_embed_id'])
            print(f'Fixed YouTube ID: {youtube_id}')
    elif not story.youtube_url:
        story.youtube_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        story.youtube_embed_id = 'dQw4w9WgXcQ'
        story.save(update_fields=['youtube_url', 'youtube_embed_id'])
        print('Set test video')
    else:
        print(f'Already has video: {story.youtube_embed_id}')
        
except Story.DoesNotExist:
    print('Story not found')

print('Fixing all stories...')
stories_fixed = 0
for story in Story.objects.filter(youtube_embed_id__isnull=True):
    if story.youtube_url:
        youtube_id = extract_youtube_id(story.youtube_url)
        if youtube_id:
            story.youtube_embed_id = youtube_id
            story.save(update_fields=['youtube_embed_id'])
            stories_fixed += 1

for story in Story.objects.filter(youtube_embed_id=''):
    if story.youtube_url:
        youtube_id = extract_youtube_id(story.youtube_url)
        if youtube_id:
            story.youtube_embed_id = youtube_id
            story.save(update_fields=['youtube_embed_id'])
            stories_fixed += 1

print(f'Fixed {stories_fixed} stories')

stories_with_video = Story.objects.exclude(youtube_embed_id__isnull=True).exclude(youtube_embed_id='').count()
stories_without_video = Story.objects.filter(youtube_embed_id__isnull=True).count() + Story.objects.filter(youtube_embed_id='').count()
print(f'With video: {stories_with_video}')
print(f'Without video: {stories_without_video}')
"

echo.
echo Fix completed!
echo Now run: python manage.py runserver
echo Then open: http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/
pause
