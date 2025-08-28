# core/seo/schema_org.py
"""
Schema.org structured data generation
"""

import json
from django.urls import reverse
from django.conf import settings
from django.db import models
from typing import Dict, List, Any


class SchemaGenerator:
    """Генератор Schema.org данных"""
    
    def __init__(self, request=None):
        self.request = request
        self.domain = getattr(settings, 'SITE_DOMAIN', 'pravoslavie-portal.ru')
        self.base_url = f"https://{self.domain}"
    
    def get_organization_schema(self) -> Dict[str, Any]:
        """Schema для организации"""
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Добрые истории",
            "description": "Православный портал с духовными рассказами, книгами и детскими сказками",
            "url": self.base_url,
            "logo": f"{self.base_url}/static/images/logo.png",
            "foundingDate": "2024",
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "customer service",
                "email": "info@pravoslavie-portal.ru",
                "url": f"{self.base_url}/contact/"
            },
            "sameAs": [
                # Добавьте ваши социальные сети
                "https://youtube.com/@your-channel",
                "https://vk.com/your-group",
                "https://t.me/your-channel"
            ]
        }
    
    def get_website_schema(self) -> Dict[str, Any]:
        """Schema для сайта"""
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Добрые истории",
            "description": "Православный портал с духовными рассказами, книгами и детскими сказками",
            "url": self.base_url,
            "potentialAction": {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": f"{self.base_url}/search/?q={{search_term_string}}"
                },
                "query-input": "required name=search_term_string"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Добрые истории",
                "url": self.base_url
            }
        }
    
    def get_book_schema(self, book) -> Dict[str, Any]:
        """Schema для книги"""
        from datetime import datetime
        
        # Безопасная обработка дат
        def format_date(date_value):
            if hasattr(date_value, 'isoformat'):
                return date_value.isoformat()
            elif isinstance(date_value, str):
                return date_value
            else:
                return datetime.now().isoformat()
        
        schema = {
            "@context": "https://schema.org",
            "@type": "Book",
            "name": book.title,
            "description": book.description,
            "url": self.base_url + reverse('books:detail', kwargs={'slug': book.slug}),
            "datePublished": format_date(book.created_at),
            "dateModified": format_date(book.updated_at),
            "genre": "Religious",
            "inLanguage": "ru",
            "isAccessibleForFree": book.price == 0,
            "publisher": {
                "@type": "Organization",
                "name": "Добрые истории",
                "url": self.base_url
            }
        }
        
        # Добавляем автора если есть
        if hasattr(book, 'author') and book.author:
            schema["author"] = {
                "@type": "Person",
                "name": book.author
            }
        
        # Добавляем изображение если есть
        if book.cover:
            schema["image"] = self.base_url + book.cover.url
        
        # Добавляем рейтинг если есть отзывы
        if hasattr(book, 'reviews') and book.reviews.exists():
            avg_rating = book.reviews.aggregate(avg=models.Avg('rating'))['avg']
            if avg_rating:
                schema["aggregateRating"] = {
                    "@type": "AggregateRating",
                    "ratingValue": round(avg_rating, 1),
                    "reviewCount": book.reviews.count(),
                    "bestRating": 5,
                    "worstRating": 1
                }
        
        # Добавляем цену если платная книга
        if book.price > 0:
            schema["offers"] = {
                "@type": "Offer",
                "price": str(book.price),
                "priceCurrency": "RUB",
                "availability": "https://schema.org/InStock",
                "seller": {
                    "@type": "Organization",
                    "name": "Добрые истории"
                }
            }
        
        return schema
    
    def get_video_schema(self, story) -> Dict[str, Any]:
        """Schema для видео-рассказа"""
        from datetime import datetime
        
        # Безопасная обработка дат
        def format_date(date_value):
            if hasattr(date_value, 'isoformat'):
                return date_value.isoformat()
            elif isinstance(date_value, str):
                return date_value
            else:
                return datetime.now().isoformat()
        
        schema = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": story.title,
            "description": story.description,
            "url": self.base_url + reverse('stories:detail', kwargs={'slug': story.slug}),
            "datePublished": format_date(story.created_at),
            "dateModified": format_date(story.updated_at),
            "genre": "Religious",
            "inLanguage": "ru",
            "isFamilyFriendly": True,
            "publisher": {
                "@type": "Organization",
                "name": "Добрые истории",
                "url": self.base_url
            }
        }
        
        # Добавляем YouTube embed если есть
        if story.youtube_embed_id:
            # Используем готовый ID видео
            youtube_id = story.youtube_embed_id
            schema["embedUrl"] = f"https://www.youtube.com/embed/{youtube_id}"
            schema["thumbnailUrl"] = f"https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg"
        
        return schema
    
    def get_article_schema(self, obj, article_type="Article") -> Dict[str, Any]:
        """Schema для статьи/контента"""
        return {
            "@context": "https://schema.org",
            "@type": article_type,
            "headline": obj.title,
            "description": getattr(obj, 'description', ''),
            "datePublished": obj.created_at.isoformat(),
            "dateModified": obj.updated_at.isoformat(),
            "author": {
                "@type": "Organization",
                "name": "Добрые истории"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Добрые истории",
                "url": self.base_url
            },
            "inLanguage": "ru"
        }
    
    def get_breadcrumb_schema(self, breadcrumbs: List[Dict[str, str]]) -> Dict[str, Any]:
        """Schema для хлебных крошек"""
        items = []
        for i, breadcrumb in enumerate(breadcrumbs, 1):
            items.append({
                "@type": "ListItem",
                "position": i,
                "name": breadcrumb['name'],
                "item": self.base_url + breadcrumb['url'] if not breadcrumb['url'].startswith('http') else breadcrumb['url']
            })
        
        return {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": items
        }


def get_schema_data(schema_type: str, obj=None, request=None, **kwargs) -> str:
    """
    Получить JSON-LD Schema.org данные
    
    Args:
        schema_type: Тип схемы ('organization', 'website', 'book', 'video', etc.)
        obj: Объект модели (для динамических схем)
        request: HTTP request
        **kwargs: Дополнительные параметры
        
    Returns:
        JSON-LD строка для вставки в HTML
    """
    generator = SchemaGenerator(request)
    
    schema_data = None
    
    if schema_type == 'organization':
        schema_data = generator.get_organization_schema()
    elif schema_type == 'website':
        schema_data = generator.get_website_schema()
    elif schema_type == 'book' and obj:
        schema_data = generator.get_book_schema(obj)
    elif schema_type == 'video' and obj:
        schema_data = generator.get_video_schema(obj)
    elif schema_type == 'article' and obj:
        schema_data = generator.get_article_schema(obj, kwargs.get('article_type', 'Article'))
    elif schema_type == 'breadcrumb' and 'breadcrumbs' in kwargs:
        schema_data = generator.get_breadcrumb_schema(kwargs['breadcrumbs'])
    
    if schema_data:
        return json.dumps(schema_data, ensure_ascii=False, indent=2)
    
    return ""


def get_combined_schema(*schemas) -> str:
    """
    Объединить несколько схем в одну JSON-LD структуру
    
    Args:
        *schemas: Список JSON-LD строк или словарей
        
    Returns:
        Объединенная JSON-LD строка
    """
    combined = []
    
    for schema in schemas:
        if isinstance(schema, str):
            try:
                combined.append(json.loads(schema))
            except json.JSONDecodeError:
                continue
        elif isinstance(schema, dict):
            combined.append(schema)
    
    if len(combined) == 1:
        return json.dumps(combined[0], ensure_ascii=False, indent=2)
    elif len(combined) > 1:
        return json.dumps(combined, ensure_ascii=False, indent=2)
    
    return ""
