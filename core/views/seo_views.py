# core/views/seo_views.py

from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.template.response import TemplateResponse


@require_GET
def robots_txt(request):
    """Генерация robots.txt файла"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Sitemaps",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        "",
        "# Disallow admin",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "",
        "# Crawl delay",
        "Crawl-delay: 1",
    ]
    
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def custom_sitemap(request):
    """Кастомный sitemap view (заглушка)"""
    # Эта функция может быть использована для кастомной логики sitemap
    # Пока возвращаем простой ответ
    return HttpResponse(
        "<?xml version='1.0' encoding='UTF-8'?>\n<urlset></urlset>",
        content_type='application/xml'
    )
