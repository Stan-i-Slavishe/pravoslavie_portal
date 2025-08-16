import django
import os
import sys

# Добавляем путь к проекту
sys.path.append(r'E:\pravoslavie_portal')

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template.loader import get_template
from django.template import TemplateDoesNotExist, TemplateSyntaxError

def check_template(template_path):
    try:
        template = get_template(template_path)
        print(f'✅ Шаблон {template_path} загружается успешно')
        return True
    except TemplateDoesNotExist as e:
        print(f'❌ Шаблон {template_path} не найден: {e}')
        return False
    except TemplateSyntaxError as e:
        print(f'❌ Синтаксическая ошибка в шаблоне {template_path}: {e}')
        return False
    except Exception as e:
        print(f'❌ Другая ошибка в шаблоне {template_path}: {e}')
        return False

if __name__ == '__main__':
    print('🔍 Проверка синтаксиса шаблонов...')
    
    templates_to_check = [
        'stories/story_detail.html',
        'base.html',
        'stories/story_list.html'
    ]
    
    all_good = True
    for template in templates_to_check:
        if not check_template(template):
            all_good = False
    
    if all_good:
        print('\n🎉 Все шаблоны проверены успешно!')
    else:
        print('\n⚠️ Есть проблемы с шаблонами!')
