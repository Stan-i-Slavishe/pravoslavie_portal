# core/seo/meta_tags.py
"""
SEO meta tags management system
"""

from django.urls import reverse
from django.conf import settings
from typing import Dict, Optional


class SEOManager:
    """Менеджер для управления SEO мета-тегами"""
    
    # Базовые настройки сайта
    SITE_CONFIG = {
        'name': 'Добрые истории',
        'description': 'Православный портал с духовными рассказами, книгами, аудио и детскими сказками',
        'keywords': 'православие, духовность, рассказы, книги, аудио, детские сказки, терапевтические сказки, православные истории',
        'author': 'Добрые истории',
        'og_type': 'website',
        'twitter_card': 'summary_large_image',
        'locale': 'ru_RU',
        'domain': 'pravoslavie-portal.ru',  # Замените на ваш домен
    }
    
    # Мета-теги для разных страниц
    PAGE_META = {
        'home': {
            'title': 'Добрые истории - Православный портал с духовными рассказами и книгами',
            'description': 'Православный портал "Добрые истории" - духовные видео-рассказы, православные книги, аудио контент и терапевтические сказки для детей. Укрепляйте веру всей семьей.',
            'keywords': 'православие, духовные рассказы, православные книги, детские сказки, духовность, вера, православный портал',
            'og_title': 'Добрые истории - Православный портал для всей семьи',
            'og_description': 'Духовные рассказы, православные книги и терапевтические сказки для укрепления веры',
        },
        
        'stories_list': {
            'title': 'Духовные видео-рассказы - Добрые истории',
            'description': 'Коллекция духовных видео-рассказов о вере, житиях святых и православных традициях. Смотрите бесплатно онлайн.',
            'keywords': 'духовные рассказы, православные видео, жития святых, духовные истории, православные фильмы',
            'og_title': 'Духовные видео-рассказы',
            'og_description': 'Смотрите духовные рассказы о вере и православных традициях',
        },
        
        'books_list': {
            'title': 'Православная библиотека книг - Добрые истории',
            'description': 'Православные книги, духовная литература и жития святых. Читайте онлайн или скачивайте в PDF формате.',
            'keywords': 'православные книги, духовная литература, жития святых, православная библиотека, скачать книги',
            'og_title': 'Православная библиотека',
            'og_description': 'Православные книги и духовная литература для чтения онлайн',
        },
        
        'fairy_tales': {
            'title': 'Терапевтические сказки для детей - Добрые истории',
            'description': 'Персонализированные терапевтические сказки для решения детских проблем, страхов и развития характера. Скоро на нашем портале.',
            'keywords': 'терапевтические сказки, детские сказки, персонализированные сказки, детская психология, детские страхи',
            'og_title': 'Терапевтические сказки для детей - Скоро',
            'og_description': 'Персонализированные сказки для решения детских проблем и развития характера',
        },
        
        'shop': {
            'title': 'Магазин православных книг и материалов - Добрые истории',
            'description': 'Покупайте православные книги, аудио материалы и цифровой контент. Безопасная оплата, мгновенная доставка.',
            'keywords': 'купить православные книги, магазин духовной литературы, православный магазин, цифровые книги',
            'og_title': 'Магазин православных материалов',
            'og_description': 'Покупайте православные книги и духовные материалы онлайн',
        },
        
        'about': {
            'title': 'О проекте "Добрые истории" - Православный портал',
            'description': 'Узнайте о миссии православного портала "Добрые истории" - создании качественного духовного контента для всей семьи.',
            'keywords': 'о проекте, православный портал, миссия, духовный контент, команда проекта',
            'og_title': 'О проекте "Добрые истории"',
            'og_description': 'Миссия создания качественного духовного контента для всей семьи',
        },
        
        'contact': {
            'title': 'Контакты - Добрые истории',
            'description': 'Свяжитесь с командой православного портала "Добрые истории". Обратная связь, предложения и сотрудничество.',
            'keywords': 'контакты, обратная связь, сотрудничество, православный портал',
            'og_title': 'Контакты',
            'og_description': 'Свяжитесь с командой православного портала',
        },
    }
    
    def __init__(self, request=None):
        self.request = request
        self.domain = getattr(settings, 'SITE_DOMAIN', self.SITE_CONFIG['domain'])
    
    def get_page_meta(self, page_key: str, **kwargs) -> Dict[str, str]:
        """
        Получить мета-теги для страницы
        
        Args:
            page_key: Ключ страницы из PAGE_META
            **kwargs: Дополнительные параметры для кастомизации
            
        Returns:
            Dict с мета-тегами
        """
        base_meta = self.PAGE_META.get(page_key, {})
        
        # Объединяем с переданными параметрами
        meta = {**base_meta, **kwargs}
        
        # Добавляем базовые настройки
        meta.setdefault('site_name', self.SITE_CONFIG['name'])
        meta.setdefault('author', self.SITE_CONFIG['author'])
        meta.setdefault('locale', self.SITE_CONFIG['locale'])
        meta.setdefault('og_type', self.SITE_CONFIG['og_type'])
        meta.setdefault('twitter_card', self.SITE_CONFIG['twitter_card'])
        
        # Генерируем canonical URL если есть request
        if self.request:
            meta['canonical_url'] = self.request.build_absolute_uri()
            meta['og_url'] = meta['canonical_url']
        
        return meta
    
    def get_dynamic_meta(self, obj, page_type='detail', **kwargs) -> Dict[str, str]:
        """
        Генерировать мета-теги для динамических объектов (книги, рассказы и т.д.)
        
        Args:
            obj: Объект модели (Book, Story, etc.)
            page_type: Тип страницы ('detail', 'list', etc.)
            **kwargs: Дополнительные параметры
            
        Returns:
            Dict с мета-тегами
        """
        model_name = obj._meta.model_name
        
        if model_name == 'book':
            return self._get_book_meta(obj, **kwargs)
        elif model_name == 'story':
            return self._get_story_meta(obj, **kwargs)
        elif model_name == 'fairytaletemplate':
            return self._get_fairy_tale_meta(obj, **kwargs)
        else:
            return self.get_page_meta('home')
    
    def _get_book_meta(self, book, **kwargs) -> Dict[str, str]:
        """Мета-теги для книг"""
        return {
            'title': f'{book.title} - Православная книга | Добрые истории',
            'description': book.description[:155] + '...' if len(book.description) > 155 else book.description,
            'keywords': f'православная книга, {book.title}, духовная литература, скачать книгу, читать онлайн',
            'og_title': book.title,
            'og_description': book.description[:155] + '...' if len(book.description) > 155 else book.description,
            'og_type': 'book',
            'book_author': getattr(book, 'author', 'Неизвестен'),
            'book_isbn': getattr(book, 'isbn', ''),
            **kwargs
        }
    
    def _get_story_meta(self, story, **kwargs) -> Dict[str, str]:
        """Мета-теги для рассказов"""
        return {
            'title': f'{story.title} - Духовный рассказ | Добрые истории',
            'description': story.description[:155] + '...' if len(story.description) > 155 else story.description,
            'keywords': f'духовный рассказ, {story.title}, православное видео, смотреть онлайн',
            'og_title': story.title,
            'og_description': story.description[:155] + '...' if len(story.description) > 155 else story.description,
            'og_type': 'video.other',
            'video_duration': getattr(story, 'duration', ''),
            **kwargs
        }
    
    def _get_fairy_tale_meta(self, fairy_tale, **kwargs) -> Dict[str, str]:
        """Мета-теги для сказок"""
        return {
            'title': f'{fairy_tale.title} - Терапевтическая сказка | Добрые истории',
            'description': fairy_tale.short_description[:155] + '...' if len(fairy_tale.short_description) > 155 else fairy_tale.short_description,
            'keywords': f'терапевтическая сказка, {fairy_tale.title}, детская сказка, персонализация',
            'og_title': fairy_tale.title,
            'og_description': fairy_tale.short_description[:155] + '...' if len(fairy_tale.short_description) > 155 else fairy_tale.short_description,
            'og_type': 'article',
            **kwargs
        }


def page_meta(page_key: str, request=None, **kwargs):
    """
    Функция-хелпер для быстрого получения мета-тегов в шаблонах
    
    Usage in views:
        context['seo'] = page_meta('home', request=request)
    """
    seo_manager = SEOManager(request)
    return seo_manager.get_page_meta(page_key, **kwargs)
