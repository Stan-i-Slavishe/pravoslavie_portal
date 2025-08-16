import re

# Читаем шаблон и ищем блок с видео
template_path = r'E:\pravoslavie_portal\templates\stories\story_detail.html'

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем строки с видео
lines = content.split('\n')
video_lines = []

for i, line in enumerate(lines, 1):
    if any(word in line.lower() for word in ['iframe', 'youtube', 'embed', 'video-container']):
        video_lines.append(f"Строка {i}: {line.strip()}")

if video_lines:
    print("Найденные строки с видео:")
    for line in video_lines:
        print(line)
else:
    print("Строки с видео не найдены")

# Ищем блок content
content_match = re.search(r'{% block content %}.*?{% endblock %}', content, re.DOTALL)
if content_match:
    print("\nБлок content найден:")
    print(content_match.group(0)[:500] + "...")
else:
    print("\nБлок content не найден")
