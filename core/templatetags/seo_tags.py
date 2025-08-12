# core/templatetags/seo_tags.py
"""
Template tags for SEO functionality
"""

from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from core.seo import page_meta, get_schema_data

register = template.Library()


@register.inclusion_tag('seo/meta_tags.html', takes_context=True)
def render_meta_tags(context, page_key=None, obj=None, **kwargs):
    """
    Рендерит мета-теги для страницы
    
    Usage:
        {% render_meta_tags 'home' %}
        {% render_meta_tags obj=book %}
        {% render_meta_tags 'books_list' title="Кастомный заголовок" %}
    """
    request = context.get('request')
    
    if obj:
        # Для динамических объектов
        from core.seo.meta_tags import SEOManager
        seo_manager = SEOManager(request)
        meta = seo_manager.get_dynamic_meta(obj, **kwargs)
    elif page_key:
        # Для статических страниц
        meta = page_meta(page_key, request=request, **kwargs)
    else:
        # Дефолтные мета-теги
        meta = page_meta('home', request=request, **kwargs)
    
    return {
        'meta': meta,
        'request': request,
    }


@register.simple_tag(takes_context=True)
def schema_ld(context, schema_type, obj=None, **kwargs):
    """
    Генерирует JSON-LD Schema.org данные
    
    Usage:
        {% schema_ld 'organization' %}
        {% schema_ld 'book' obj=book %}
        {% schema_ld 'breadcrumb' breadcrumbs=breadcrumbs %}
    """
    request = context.get('request')
    schema_json = get_schema_data(schema_type, obj=obj, request=request, **kwargs)
    
    if schema_json:
        return mark_safe(f'<script type="application/ld+json">\n{schema_json}\n</script>')
    
    return ""


@register.simple_tag
def canonical_url(request, url_name=None, **kwargs):
    """
    Генерирует canonical URL
    
    Usage:
        {% canonical_url request %}
        {% canonical_url request 'books:detail' slug=book.slug %}
    """
    if url_name:
        try:
            path = reverse(url_name, kwargs=kwargs)
            return request.build_absolute_uri(path)
        except:
            return request.build_absolute_uri()
    else:
        return request.build_absolute_uri()


@register.inclusion_tag('seo/breadcrumbs.html', takes_context=True)
def render_breadcrumbs(context, breadcrumbs=None):
    """
    Рендерит хлебные крошки
    
    Usage:
        {% render_breadcrumbs breadcrumbs %}
        
    Где breadcrumbs - список словарей:
    [
        {'name': 'Главная', 'url': '/'},
        {'name': 'Книги', 'url': '/books/'},
        {'name': 'Название книги', 'url': ''}  # Пустой URL для текущей страницы
    ]
    """
    if not breadcrumbs:
        breadcrumbs = [{'name': 'Главная', 'url': '/'}]
    
    return {
        'breadcrumbs': breadcrumbs,
        'request': context.get('request'),
    }


@register.simple_tag
def page_title(base_title, site_name="Добрые истории"):
    """
    Генерирует правильный заголовок страницы
    
    Usage:
        {% page_title "Название страницы" %}
        {% page_title book.title "Православные книги" %}
    """
    if base_title and base_title != site_name:
        return f"{base_title} | {site_name}"
    else:
        return site_name


@register.filter
def truncate_description(text, length=155):
    """
    Обрезает описание до нужной длины для meta description
    
    Usage:
        {{ book.description|truncate_description:160 }}
    """
    if not text:
        return ""
    
    if len(text) <= length:
        return text
    
    # Обрезаем по словам
    words = text[:length].split()
    if len(words) > 1:
        words = words[:-1]  # Убираем последнее неполное слово
    
    result = ' '.join(words)
    return result + '...' if result != text else result


@register.simple_tag
def social_image_url(request, obj=None, default_image="/static/images/og-default.jpg"):
    """
    Генерирует URL изображения для социальных сетей
    
    Usage:
        {% social_image_url request obj=book %}
        {% social_image_url request default_image="/static/images/custom-og.jpg" %}
    """
    base_url = request.build_absolute_uri('/')[:-1]  # Убираем последний слеш
    
    # Пытаемся найти изображение у объекта
    if obj:
        for attr in ['cover', 'cover_image', 'image', 'thumbnail', 'photo']:
            if hasattr(obj, attr):
                image_field = getattr(obj, attr)
                if image_field:
                    return base_url + image_field.url
    
    # Возвращаем дефолтное изображение
    return base_url + default_image
