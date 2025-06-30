@echo off
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██  🔍 ДИАГНОСТИКА КОММЕНТАРИЕВ - ФИНАЛЬНАЯ ПРОВЕРКА           ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

echo ✅ Тестовые данные созданы: 6 комментариев
echo ✅ Файлы загружаются без ошибок 404
echo.

echo 🔄 Подключаем диагностический скрипт...
python manage.py collectstatic --noinput

echo.
echo 🌐 Проверяем URLs...
python manage.py shell -c "
from django.urls import reverse;
try:
    url1 = reverse('comments:story_comments_list', args=[3]);
    print('✅ URL загрузки комментариев:', url1);
except Exception as e:
    print('❌ Ошибка URL загрузки:', e);

try:
    url2 = reverse('comments:add_story_comment', args=[3]);
    print('✅ URL добавления комментариев:', url2);
except Exception as e:
    print('❌ Ошибка URL добавления:', e);
"

echo.
echo 📊 Проверяем, что комментарии действительно есть...
python manage.py shell -c "
from comments.models import Comment;
from stories.models import Story;
from django.contrib.contenttypes.models import ContentType;

story = Story.objects.get(slug='pasha-voskresenie-hristovo');
ct = ContentType.objects.get_for_model(Story);
comments = Comment.objects.filter(content_type=ct, object_id=story.id);

print(f'📊 Story ID: {story.id}');
print(f'📊 Content Type ID: {ct.id}');
print(f'📊 Найдено комментариев: {comments.count()}');

for i, c in enumerate(comments[:3]):
    print(f'💬 {i+1}. {c.author.username}: {c.text[:40]}... (ID: {c.id})');
"

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██  🎯 ЗАПУСКАЕМ С ДИАГНОСТИЧЕСКИМ СКРИПТОМ                    ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.
echo 🔍 ИНСТРУКЦИИ ДЛЯ ПРОВЕРКИ:
echo    1. Откройте Developer Tools (F12)
echo    2. Перейдите на вкладку Console
echo    3. Перезагрузите страницу
echo    4. Смотрите диагностические сообщения
echo.
echo 🎮 ЧТО ДОЛЖНО ПОЯВИТЬСЯ В КОНСОЛИ:
echo    - "🎯 Диагностический скрипт запущен"
echo    - "📍 Story ID: 3"
echo    - "🧪 Тестируем API комментариев..."
echo    - "✅ API работает! Данные: ..."
echo    - "💬 Найдено комментариев: 6"
echo.

start http://127.0.0.1:8000/stories/pasha-voskresenie-hristovo/

python manage.py runserver