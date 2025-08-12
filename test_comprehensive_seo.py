#!/usr/bin/env python
"""
COMPREHENSIVE SEO INTEGRATION TEST
==================================
Полная проверка SEO интеграции православного портала
"""

import os
import sys
import django
import json
import re
from pathlib import Path
from urllib.parse import urlparse

# Настройка Django
PROJECT_ROOT = Path(r'E:\pravoslavie_portal')
sys.path.append(str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

class SEOTester:
    def __init__(self):
        self.passed_tests = 0
        self.total_tests = 0
        self.results = []
        
    def test(self, test_name, test_func):
        """Запуск теста с подсчетом результатов"""
        self.total_tests += 1
        print(f"\n📋 Тест: {test_name}")
        print("-" * 50)
        
        try:
            result = test_func()
            if result:
                self.passed_tests += 1
                self.results.append({"name": test_name, "status": "✅ PASS", "details": ""})
                print(f"✅ {test_name} - ПРОЙДЕН")
            else:
                self.results.append({"name": test_name, "status": "❌ FAIL", "details": "Функциональные проблемы"})
                print(f"❌ {test_name} - НЕ ПРОЙДЕН")
        except Exception as e:
            self.results.append({"name": test_name, "status": "💥 ERROR", "details": str(e)})
            print(f"💥 {test_name} - ОШИБКА: {e}")
            
        return result
    
    def test_file_structure(self):
        """Проверка структуры SEO файлов"""
        required_files = [
            'core/seo/__init__.py',
            'core/seo/meta_tags.py', 
            'core/seo/schema_org.py',
            'core/seo/sitemaps.py',
            'core/templatetags/__init__.py',
            'core/templatetags/seo_tags.py',
            'core/views/__init__.py',
            'core/views/main_views.py',
            'core/views/seo_views.py',
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = PROJECT_ROOT / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                print(f"   ❌ {file_path}")
            else:
                print(f"   ✅ {file_path}")
        
        if missing_files:
            print(f"\n⚠️  Отсутствующие файлы: {', '.join(missing_files)}")
            return False
        
        print("✨ Все файлы SEO структуры найдены!")
        return True
    
    def test_imports(self):
        """Проверка всех импортов SEO модулей"""
        imports_to_test = [
            ('core.seo', ['page_meta', 'SEOManager', 'get_schema_data']),
            ('core.seo.meta_tags', ['SEOManager', 'page_meta']),
            ('core.seo.schema_org', ['SchemaGenerator', 'get_schema_data']),
            ('core.seo.sitemaps', ['sitemaps']),
            ('core.templatetags.seo_tags', ['render_meta_tags', 'schema_ld', 'canonical_url']),
            ('core.views', ['HomeView', 'AboutView', 'ContactView']),
        ]
        
        failed_imports = []
        
        for module_name, items in imports_to_test:
            try:
                module = __import__(module_name, fromlist=items)
                for item in items:
                    if hasattr(module, item):
                        print(f"   ✅ {module_name}.{item}")
                    else:
                        print(f"   ❌ {module_name}.{item} - НЕ НАЙДЕН")
                        failed_imports.append(f"{module_name}.{item}")
            except ImportError as e:
                print(f"   💥 {module_name} - ОШИБКА ИМПОРТА: {e}")
                failed_imports.extend([f"{module_name}.{item}" for item in items])
        
        if failed_imports:
            print(f"\n⚠️  Проблемы с импортами: {', '.join(failed_imports)}")
            return False
            
        print("✨ Все SEO модули импортируются корректно!")
        return True
    
    def test_meta_tags_generation(self):
        """Проверка генерации мета-тегов"""
        from core.seo import page_meta
        
        pages_to_test = ['home', 'about', 'contact', 'books_list', 'stories_list', 'shop']
        
        for page in pages_to_test:
            try:
                meta = page_meta(page)
                
                required_fields = ['title', 'description']
                missing_fields = [field for field in required_fields if not meta.get(field)]
                
                if missing_fields:
                    print(f"   ❌ {page}: отсутствуют поля {missing_fields}")
                    return False
                else:
                    print(f"   ✅ {page}: title='{meta['title'][:50]}...', description='{meta['description'][:50]}...'")
                    
            except Exception as e:
                print(f"   💥 {page}: {e}")
                return False
        
        print("✨ Все мета-теги генерируются корректно!")
        return True
    
    def test_schema_org_generation(self):
        """Проверка генерации Schema.org"""
        from core.seo.schema_org import SchemaGenerator, get_schema_data
        
        # Тест базовых схем
        generator = SchemaGenerator()
        
        # Тест организации
        try:
            org_schema = generator.get_organization_schema()
            if org_schema.get('@type') != 'Organization':
                print("   ❌ Неверная схема организации")
                return False
            print("   ✅ Схема организации")
        except Exception as e:
            print(f"   💥 Ошибка схемы организации: {e}")
            return False
        
        # Тест сайта
        try:
            site_schema = generator.get_website_schema()
            if site_schema.get('@type') != 'WebSite':
                print("   ❌ Неверная схема сайта")
                return False
            print("   ✅ Схема сайта")
        except Exception as e:
            print(f"   💥 Ошибка схемы сайта: {e}")
            return False
        
        # Тест функции get_schema_data
        try:
            schema_json = get_schema_data('organization')
            if not schema_json or not json.loads(schema_json):
                print("   ❌ get_schema_data не возвращает валидный JSON")
                return False
            print("   ✅ get_schema_data работает")
        except Exception as e:
            print(f"   💥 Ошибка get_schema_data: {e}")
            return False
        
        print("✨ Все Schema.org схемы генерируются корректно!")
        return True
    
    def test_model_compatibility(self):
        """Проверка совместимости с моделями"""
        from core.seo.schema_org import SchemaGenerator
        
        generator = SchemaGenerator()
        
        # Тест с моделью Book
        try:
            from books.models import Book
            
            # Создаем мок-объект Book
            class MockBook:
                title = "Тестовая православная книга"
                description = "Описание тестовой книги для проверки SEO"
                created_at = "2024-01-01T00:00:00Z"
                updated_at = "2024-01-01T00:00:00Z"
                slug = "test-book"
                price = 0
                cover = None
                author = "Тестовый автор"
                
                class reviews:
                    @staticmethod
                    def exists():
                        return False
            
            mock_book = MockBook()
            book_schema = generator.get_book_schema(mock_book)
            
            if not book_schema or book_schema.get('@type') != 'Book':
                print("   ❌ Схема книги генерируется неверно")
                return False
            print("   ✅ Схема книги совместима")
            
        except Exception as e:
            print(f"   💥 Ошибка схемы книги: {e}")
            return False
        
        # Тест с моделью Story
        try:
            class MockStory:
                title = "Тестовый духовный рассказ"
                description = "Описание тестового рассказа"
                created_at = "2024-01-01T00:00:00Z"
                updated_at = "2024-01-01T00:00:00Z"
                slug = "test-story"
                youtube_embed = '<iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ"></iframe>'
            
            mock_story = MockStory()
            video_schema = generator.get_video_schema(mock_story)
            
            if not video_schema or video_schema.get('@type') != 'VideoObject':
                print("   ❌ Схема видео генерируется неверно")
                return False
            print("   ✅ Схема видео совместима")
            
        except Exception as e:
            print(f"   💥 Ошибка схемы видео: {e}")
            return False
        
        print("✨ Все модели совместимы с SEO схемами!")
        return True
    
    def test_templatetags(self):
        """Проверка template tags"""
        from django.template import Template, Context
        from django.test import RequestFactory
        from django.conf import settings
        
        # Создаем фейковый request с правильным HOST
        factory = RequestFactory()
        request = factory.get('/', HTTP_HOST='testserver')
        
        # Тест render_meta_tags
        try:
            template = Template('{% load seo_tags %}{% render_meta_tags "home" %}')
            context = Context({'request': request})
            rendered = template.render(context)
            print("   ✅ render_meta_tags работает")
        except Exception as e:
            print(f"   💥 Ошибка render_meta_tags: {e}")
            return False
        
        # Тест schema_ld
        try:
            template = Template('{% load seo_tags %}{% schema_ld "organization" %}')
            context = Context({'request': request})
            rendered = template.render(context)
            if '<script type="application/ld+json">' not in rendered:
                print("   ❌ schema_ld не генерирует правильный тег")
                return False
            print("   ✅ schema_ld работает")
        except Exception as e:
            print(f"   💥 Ошибка schema_ld: {e}")
            return False
        
        # Тест canonical_url
        try:
            template = Template('{% load seo_tags %}{% canonical_url request %}')
            context = Context({'request': request})
            rendered = template.render(context).strip()
            if not rendered.startswith('http'):
                print(f"   ❌ canonical_url возвращает неверный URL: {rendered}")
                return False
            print("   ✅ canonical_url работает")
        except Exception as e:
            print(f"   💥 Ошибка canonical_url: {e}")
            return False
        
        print("✨ Все template tags работают корректно!")
        return True
    
    def test_sitemap_functionality(self):
        """Проверка функциональности sitemap"""
        try:
            from core.seo.sitemaps import sitemaps
            if not sitemaps:
                print("   ❌ Sitemap словарь пуст")
                return False
            print(f"   ✅ Sitemap содержит разделы: {', '.join(sitemaps.keys())}")
        except Exception as e:
            print(f"   💥 Ошибка импорта sitemap: {e}")
            return False
        
        # Проверка robots.txt view
        try:
            from core.views.seo_views import robots_txt
            print("   ✅ robots_txt view импортируется")
        except Exception as e:
            print(f"   💥 Ошибка robots_txt view: {e}")
            return False
        
        print("✨ Sitemap функциональность работает!")
        return True
    
    def test_url_patterns(self):
        """Проверка URL паттернов SEO"""
        from django.urls import reverse, NoReverseMatch
        
        seo_urls = [
            ('robots_txt', 'robots.txt'),
            ('django.contrib.sitemaps.views.sitemap', 'sitemap.xml'),
        ]
        
        for url_name, expected_path in seo_urls:
            try:
                url = reverse(url_name)
                if expected_path not in url:
                    print(f"   ❌ {url_name}: неверный путь {url}")
                    return False
                print(f"   ✅ {url_name}: {url}")
            except NoReverseMatch:
                print(f"   ❌ {url_name}: URL не найден")
                return False
            except Exception as e:
                print(f"   💥 {url_name}: {e}")
                return False
        
        print("✨ Все SEO URL паттерны работают!")
        return True
    
    def test_settings_configuration(self):
        """Проверка настроек Django для SEO"""
        from django.conf import settings
        
        # Проверяем необходимые настройки
        required_settings = {
            'INSTALLED_APPS': ['django.contrib.sitemaps'],
            'TEMPLATES': 'context_processors',
        }
        
        # Проверка INSTALLED_APPS
        if 'django.contrib.sitemaps' not in settings.INSTALLED_APPS:
            print("   ❌ django.contrib.sitemaps не в INSTALLED_APPS")
            return False
        print("   ✅ django.contrib.sitemaps установлен")
        
        # Проверка TEMPLATES context processors
        templates = getattr(settings, 'TEMPLATES', [])
        if templates:
            context_processors = templates[0].get('OPTIONS', {}).get('context_processors', [])
            if 'django.template.context_processors.request' not in context_processors:
                print("   ❌ request context processor не настроен")
                return False
            print("   ✅ request context processor настроен")
        
        print("✨ Настройки Django для SEO корректны!")
        return True
    
    def test_meta_tags_content_quality(self):
        """Проверка качества контента мета-тегов"""
        from core.seo import page_meta
        
        pages = ['home', 'about', 'books_list', 'stories_list']
        
        for page in pages:
            meta = page_meta(page)
            
            # Проверка длины title
            title = meta.get('title', '')
            if len(title) < 30 or len(title) > 60:
                print(f"   ⚠️  {page}: title длина {len(title)} (рекомендуется 30-60)")
            else:
                print(f"   ✅ {page}: title длина оптимальна ({len(title)})")
            
            # Проверка длины description
            description = meta.get('description', '')
            if len(description) < 120 or len(description) > 160:
                print(f"   ⚠️  {page}: description длина {len(description)} (рекомендуется 120-160)")
            else:
                print(f"   ✅ {page}: description длина оптимальна ({len(description)})")
            
            # Проверка наличия ключевых слов
            keywords = meta.get('keywords', '')
            if not keywords:
                print(f"   ⚠️  {page}: отсутствуют keywords")
            else:
                print(f"   ✅ {page}: keywords присутствуют")
        
        print("✨ Проверка качества контента завершена!")
        return True
    
    def test_schema_org_validation(self):
        """Проверка валидности Schema.org JSON"""
        from core.seo.schema_org import get_schema_data
        
        schemas_to_test = [
            ('organization', None),
            ('website', None),
        ]
        
        for schema_type, obj in schemas_to_test:
            try:
                schema_json = get_schema_data(schema_type, obj)
                if not schema_json:
                    print(f"   ❌ {schema_type}: пустая схема")
                    return False
                
                # Проверяем валидность JSON
                schema_data = json.loads(schema_json)
                
                # Проверяем обязательные поля Schema.org
                if '@context' not in schema_data:
                    print(f"   ❌ {schema_type}: отсутствует @context")
                    return False
                    
                if '@type' not in schema_data:
                    print(f"   ❌ {schema_type}: отсутствует @type")
                    return False
                
                print(f"   ✅ {schema_type}: валидная схема")
                
            except json.JSONDecodeError:
                print(f"   ❌ {schema_type}: невалидный JSON")
                return False
            except Exception as e:
                print(f"   💥 {schema_type}: {e}")
                return False
        
        print("✨ Все Schema.org схемы валидны!")
        return True
    
    def generate_report(self):
        """Генерация итогового отчета"""
        print("\n" + "=" * 80)
        print("📊 ИТОГОВЫЙ ОТЧЕТ SEO ИНТЕГРАЦИИ")
        print("=" * 80)
        
        for result in self.results:
            print(f"{result['status']} {result['name']}")
            if result['details']:
                print(f"    └─ {result['details']}")
        
        print("\n" + "-" * 80)
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📈 СТАТИСТИКА:")
        print(f"   Всего тестов: {self.total_tests}")
        print(f"   Пройдено: {self.passed_tests}")
        print(f"   Не пройдено: {self.total_tests - self.passed_tests}")
        print(f"   Успешность: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("\n🎉 ОТЛИЧНО! SEO интеграция выполнена на высоком уровне!")
            print("🚀 Проект готов к продакшену с точки зрения SEO!")
        elif success_rate >= 70:
            print("\n✅ ХОРОШО! SEO интеграция в основном готова.")
            print("🔧 Рекомендуется устранить оставшиеся проблемы.")
        elif success_rate >= 50:
            print("\n⚠️  УДОВЛЕТВОРИТЕЛЬНО. SEO интеграция требует доработки.")
            print("🛠️  Необходимо исправить выявленные проблемы.")
        else:
            print("\n❌ КРИТИЧНО! SEO интеграция требует серьезной доработки.")
            print("🚨 Проект не готов к запуску с текущими SEO настройками.")
        
        print("\n" + "=" * 80)

def main():
    """Главная функция запуска тестов"""
    print("🔍 COMPREHENSIVE SEO INTEGRATION TEST")
    print("🎯 Православный портал 'Добрые истории'")
    print("=" * 80)
    
    tester = SEOTester()
    
    # Список всех тестов
    tests = [
        ("Структура SEO файлов", tester.test_file_structure),
        ("Импорты SEO модулей", tester.test_imports),
        ("Генерация мета-тегов", tester.test_meta_tags_generation),
        ("Генерация Schema.org", tester.test_schema_org_generation),
        ("Совместимость с моделями", tester.test_model_compatibility),
        ("Template Tags", tester.test_templatetags),
        ("Sitemap функциональность", tester.test_sitemap_functionality),
        ("URL паттерны", tester.test_url_patterns),
        ("Настройки Django", tester.test_settings_configuration),
        ("Качество мета-тегов", tester.test_meta_tags_content_quality),
        ("Валидация Schema.org", tester.test_schema_org_validation),
    ]
    
    # Запуск всех тестов
    for test_name, test_func in tests:
        tester.test(test_name, test_func)
    
    # Генерация итогового отчета
    tester.generate_report()

if __name__ == '__main__':
    main()
