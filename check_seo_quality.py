#!/usr/bin/env python
"""
SEO QUALITY METRICS CHECKER
===========================
Проверка качества SEO элементов по стандартам Google
"""

import os
import sys
import django
from pathlib import Path
import re

# Настройка Django
PROJECT_ROOT = Path(r'E:\pravoslavie_portal')
sys.path.append(str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

class SEOQualityChecker:
    def __init__(self):
        self.issues = []
        self.recommendations = []
        
    def check_title_quality(self, title, page_name):
        """Проверка качества title тегов"""
        issues = []
        recommendations = []
        
        if not title:
            issues.append("Отсутствует title")
            return issues, recommendations
            
        length = len(title)
        
        # Проверки длины
        if length < 30:
            issues.append(f"Title слишком короткий ({length} символов, рекомендуется 30-60)")
        elif length > 60:
            issues.append(f"Title слишком длинный ({length} символов, рекомендуется 30-60)")
        else:
            recommendations.append(f"Title оптимальной длины ({length} символов)")
        
        # Проверки содержания
        if not re.search(r'православ|духов|добр|истор|сказк', title.lower()):
            recommendations.append("Рассмотрите добавление ключевых слов: православный, духовный, добрые истории")
        
        # Проверка на дублирование
        if title.count('|') > 1:
            issues.append("Слишком много разделителей в title")
        
        # Проверка бренда
        if 'добрые истории' not in title.lower():
            recommendations.append("Рассмотрите добавление названия бренда 'Добрые истории'")
            
        return issues, recommendations
    
    def check_description_quality(self, description, page_name):
        """Проверка качества meta description"""
        issues = []
        recommendations = []
        
        if not description:
            issues.append("Отсутствует meta description")
            return issues, recommendations
            
        length = len(description)
        
        # Проверки длины
        if length < 120:
            issues.append(f"Description слишком короткий ({length} символов, рекомендуется 120-160)")
        elif length > 160:
            issues.append(f"Description слишком длинный ({length} символов, рекомендуется 120-160)")
        else:
            recommendations.append(f"Description оптимальной длины ({length} символов)")
        
        # Проверки содержания
        if not re.search(r'православ|духов|добр|истор|сказк|книг|рассказ', description.lower()):
            recommendations.append("Добавьте больше релевантных ключевых слов")
        
        # Проверка призыва к действию
        action_words = ['читайте', 'смотрите', 'слушайте', 'скачивайте', 'покупайте', 'изучайте']
        if not any(word in description.lower() for word in action_words):
            recommendations.append("Добавьте призыв к действию (читайте, смотрите, скачивайте)")
        
        # Проверка на дублирование с title
        if description == page_name:
            issues.append("Description дублирует title")
            
        return issues, recommendations
    
    def check_keywords_quality(self, keywords, page_name):
        """Проверка качества keywords"""
        issues = []
        recommendations = []
        
        if not keywords:
            recommendations.append("Добавьте meta keywords для лучшего понимания контента")
            return issues, recommendations
        
        keywords_list = [k.strip() for k in keywords.split(',')]
        
        # Проверка количества
        if len(keywords_list) > 10:
            issues.append(f"Слишком много keywords ({len(keywords_list)}, рекомендуется 5-10)")
        elif len(keywords_list) < 3:
            recommendations.append(f"Добавьте больше keywords (текущее: {len(keywords_list)}, рекомендуется 5-10)")
        
        # Проверка релевантности
        orthodox_keywords = ['православие', 'духовность', 'вера', 'церковь', 'святые', 'молитва']
        content_keywords = ['книги', 'рассказы', 'сказки', 'аудио', 'истории', 'чтение']
        
        has_orthodox = any(kw in keywords.lower() for kw in orthodox_keywords)
        has_content = any(kw in keywords.lower() for kw in content_keywords)
        
        if not has_orthodox:
            recommendations.append("Добавьте православные ключевые слова: православие, духовность, вера")
        if not has_content:
            recommendations.append("Добавьте контентные ключевые слова: книги, рассказы, аудио")
            
        return issues, recommendations
    
    def check_page_meta_quality(self):
        """Проверка качества мета-тегов всех страниц"""
        from core.seo import page_meta
        
        pages_to_check = {
            'home': 'Главная страница',
            'about': 'О проекте', 
            'contact': 'Контакты',
            'books_list': 'Каталог книг',
            'stories_list': 'Видео-рассказы',
            'shop': 'Магазин',
            'fairy_tales': 'Терапевтические сказки'
        }
        
        print("🔍 Проверка качества мета-тегов...")
        print("-" * 60)
        
        total_issues = 0
        total_recommendations = 0
        
        for page_key, page_name in pages_to_check.items():
            try:
                meta = page_meta(page_key)
                
                print(f"\n📄 {page_name} ({page_key}):")
                
                # Проверка title
                title_issues, title_recs = self.check_title_quality(meta.get('title', ''), page_name)
                if title_issues:
                    for issue in title_issues:
                        print(f"   ❌ Title: {issue}")
                        total_issues += 1
                else:
                    print(f"   ✅ Title: '{meta.get('title', '')[:50]}...'")
                
                for rec in title_recs:
                    print(f"   💡 Title: {rec}")
                    total_recommendations += 1
                
                # Проверка description
                desc_issues, desc_recs = self.check_description_quality(meta.get('description', ''), page_name)
                if desc_issues:
                    for issue in desc_issues:
                        print(f"   ❌ Description: {issue}")
                        total_issues += 1
                else:
                    print(f"   ✅ Description: '{meta.get('description', '')[:50]}...'")
                
                for rec in desc_recs:
                    print(f"   💡 Description: {rec}")
                    total_recommendations += 1
                
                # Проверка keywords
                kw_issues, kw_recs = self.check_keywords_quality(meta.get('keywords', ''), page_name)
                if kw_issues:
                    for issue in kw_issues:
                        print(f"   ❌ Keywords: {issue}")
                        total_issues += 1
                elif meta.get('keywords'):
                    print(f"   ✅ Keywords: {len(meta.get('keywords', '').split(','))} ключевых слов")
                
                for rec in kw_recs:
                    print(f"   💡 Keywords: {rec}")
                    total_recommendations += 1
                    
            except Exception as e:
                print(f"   💥 Ошибка проверки {page_key}: {e}")
                total_issues += 1
        
        return total_issues, total_recommendations
    
    def check_schema_org_quality(self):
        """Проверка качества Schema.org данных"""
        from core.seo.schema_org import get_schema_data
        import json
        
        print("\n🏗️  Проверка качества Schema.org...")
        print("-" * 60)
        
        schema_checks = [
            ('organization', 'Организация'),
            ('website', 'Веб-сайт'),
        ]
        
        issues = 0
        recommendations = 0
        
        for schema_type, name in schema_checks:
            try:
                schema_json = get_schema_data(schema_type)
                if not schema_json:
                    print(f"   ❌ {name}: схема не генерируется")
                    issues += 1
                    continue
                
                schema_data = json.loads(schema_json)
                
                print(f"\n🔍 {name} Schema:")
                
                # Базовые проверки
                required_fields = ['@context', '@type', 'name', 'description', 'url']
                missing_fields = [field for field in required_fields if field not in schema_data]
                
                if missing_fields:
                    print(f"   ❌ Отсутствуют обязательные поля: {', '.join(missing_fields)}")
                    issues += len(missing_fields)
                else:
                    print(f"   ✅ Все обязательные поля присутствуют")
                
                # Качественные проверки
                if schema_data.get('description') and len(schema_data['description']) < 50:
                    print(f"   💡 Описание слишком короткое ({len(schema_data['description'])} символов)")
                    recommendations += 1
                
                if schema_type == 'organization':
                    org_recommendations = []
                    if 'logo' not in schema_data:
                        org_recommendations.append("Добавьте логотип организации")
                    if 'contactPoint' not in schema_data:
                        org_recommendations.append("Добавьте контактную информацию")
                    if 'sameAs' not in schema_data:
                        org_recommendations.append("Добавьте ссылки на социальные сети")
                    
                    for rec in org_recommendations:
                        print(f"   💡 {rec}")
                        recommendations += 1
                
                elif schema_type == 'website':
                    if 'potentialAction' not in schema_data:
                        print(f"   💡 Добавьте SearchAction для поиска по сайту")
                        recommendations += 1
                        
            except Exception as e:
                print(f"   💥 Ошибка проверки {name}: {e}")
                issues += 1
        
        return issues, recommendations
    
    def check_seo_technical_quality(self):
        """Проверка технических аспектов SEO"""
        print("\n🔧 Проверка технических аспектов SEO...")
        print("-" * 60)
        
        issues = 0
        recommendations = 0
        
        # Проверка настроек Django
        from django.conf import settings
        
        print("\n⚙️  Настройки Django:")
        
        # ALLOWED_HOSTS
        if hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
            if 'localhost' in settings.ALLOWED_HOSTS and len(settings.ALLOWED_HOSTS) == 1:
                print("   💡 Настройте ALLOWED_HOSTS для продакшена")
                recommendations += 1
            else:
                print("   ✅ ALLOWED_HOSTS настроен")
        else:
            print("   ❌ ALLOWED_HOSTS не настроен")
            issues += 1
        
        # SECURE_SSL_REDIRECT
        if not getattr(settings, 'SECURE_SSL_REDIRECT', False):
            print("   💡 Включите SECURE_SSL_REDIRECT для HTTPS")
            recommendations += 1
        else:
            print("   ✅ SECURE_SSL_REDIRECT включен")
        
        # Проверка sitemap
        print("\n🗺️  Sitemap:")
        try:
            from core.seo.sitemaps import sitemaps
            if sitemaps:
                print(f"   ✅ Sitemap настроен с {len(sitemaps)} разделами")
            else:
                print("   ❌ Sitemap пуст")
                issues += 1
        except Exception as e:
            print(f"   ❌ Ошибка sitemap: {e}")
            issues += 1
        
        # Проверка robots.txt
        print("\n🤖 Robots.txt:")
        try:
            from core.views.seo_views import robots_txt
            print("   ✅ robots.txt view настроен")
        except Exception as e:
            print(f"   ❌ Ошибка robots.txt: {e}")
            issues += 1
        
        return issues, recommendations
    
    def generate_quality_report(self, meta_issues, meta_recs, schema_issues, schema_recs, tech_issues, tech_recs):
        """Генерация итогового отчета по качеству"""
        print("\n" + "=" * 80)
        print("📊 ОТЧЕТ ПО КАЧЕСТВУ SEO")
        print("=" * 80)
        
        total_issues = meta_issues + schema_issues + tech_issues
        total_recommendations = meta_recs + schema_recs + tech_recs
        
        print(f"\n📈 ОБЩАЯ СТАТИСТИКА:")
        print(f"   Критические проблемы: {total_issues}")
        print(f"   Рекомендации: {total_recommendations}")
        
        print(f"\n📋 ДЕТАЛИЗАЦИЯ:")
        print(f"   Мета-теги - проблемы: {meta_issues}, рекомендации: {meta_recs}")
        print(f"   Schema.org - проблемы: {schema_issues}, рекомендации: {schema_recs}")
        print(f"   Технические - проблемы: {tech_issues}, рекомендации: {tech_recs}")
        
        # Оценка качества
        if total_issues == 0:
            if total_recommendations <= 5:
                grade = "🏆 ОТЛИЧНО"
                color = "Зеленый"
            else:
                grade = "✅ ХОРОШО"
                color = "Светло-зеленый"
        elif total_issues <= 3:
            grade = "⚠️  УДОВЛЕТВОРИТЕЛЬНО"
            color = "Желтый"
        else:
            grade = "❌ ТРЕБУЕТ ДОРАБОТКИ"
            color = "Красный"
        
        print(f"\n🎯 ОБЩАЯ ОЦЕНКА КАЧЕСТВА SEO: {grade}")
        
        print(f"\n💡 ПРИОРИТЕТНЫЕ ДЕЙСТВИЯ:")
        if total_issues > 0:
            print(f"   1. Исправьте {total_issues} критических проблем")
        if total_recommendations > 10:
            print(f"   2. Реализуйте топ-5 рекомендаций из {total_recommendations}")
        if total_issues == 0 and total_recommendations <= 5:
            print(f"   🎉 SEO готово к продакшену! Можно запускать.")
        else:
            print(f"   3. Повторите audit после исправлений")

def main():
    """Главная функция"""
    print("📊 SEO QUALITY METRICS CHECKER")
    print("🎯 Православный портал 'Добрые истории'")
    print("=" * 80)
    
    checker = SEOQualityChecker()
    
    # Проверка мета-тегов
    meta_issues, meta_recs = checker.check_page_meta_quality()
    
    # Проверка Schema.org
    schema_issues, schema_recs = checker.check_schema_org_quality()
    
    # Проверка технических аспектов
    tech_issues, tech_recs = checker.check_seo_technical_quality()
    
    # Генерация отчета
    checker.generate_quality_report(meta_issues, meta_recs, schema_issues, schema_recs, tech_issues, tech_recs)

if __name__ == '__main__':
    main()
