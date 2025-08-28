# core/seo/sitemaps.py
"""
XML Sitemap generation for SEO
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from books.models import Book
from stories.models import Story
# from fairy_tales.models import FairyTaleTemplate  # Раскомментировать когда запустим сказки


class StaticViewSitemap(Sitemap):
    """Sitemap для статических страниц"""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return [
            'core:home',
            'core:about', 
            'core:contact',
            'stories:list',
            'books:list',
            'fairy_tales:list',  # Заглушка сказок
            'shop:catalog',
        ]
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()


class BookSitemap(Sitemap):
    """Sitemap для книг"""
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        return Book.objects.filter(is_published=True).order_by('-updated_at')
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return reverse('books:detail', kwargs={'slug': obj.slug})


class StorySitemap(Sitemap):
    """Sitemap для рассказов"""
    changefreq = 'weekly'
    priority = 0.6
    
    def items(self):
        return Story.objects.filter(is_published=True).order_by('-updated_at')
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return reverse('stories:detail', kwargs={'slug': obj.slug})


# БУДУЩЕЕ: Раскомментировать когда запустим сказки
"""
class FairyTaleSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return FairyTaleTemplate.objects.filter(is_published=True).order_by('-updated_at')
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return reverse('fairy_tales:detail', kwargs={'slug': obj.slug})
"""


class CategorySitemap(Sitemap):
    """Sitemap для категорий"""
    changefreq = 'monthly'
    priority = 0.5
    
    def items(self):
        # Импортируем здесь чтобы избежать циклических импортов
        from core.models import Category
        return Category.objects.all().order_by('name')
    
    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else timezone.now()
    
    def location(self, obj):
        return reverse('core:category_detail', kwargs={'slug': obj.slug})


# Словарь всех sitemap'ов
sitemaps = {
    'static': StaticViewSitemap,
    'books': BookSitemap,
    'stories': StorySitemap,
    'categories': CategorySitemap,
    # 'fairy_tales': FairyTaleSitemap,  # Раскомментировать позже
}


def generate_sitemap():
    """
    Генерация дополнительной информации для sitemap
    Можно использовать для кастомной генерации или статистики
    """
    stats = {
        'books_count': Book.objects.filter(is_published=True).count(),
        'stories_count': Story.objects.filter(is_published=True).count(),
        'last_update': timezone.now(),
    }
    
    return stats
