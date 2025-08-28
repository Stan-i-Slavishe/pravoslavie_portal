# core/views/__init__.py

# Импортируем все основные views
from .main_views import (
    HomeView, 
    AboutView, 
    ContactView,
    CategoryListView,
    CategoryDetailView,
    TagListView,
    TagDetailView,
    custom_404_view,
    custom_500_view
)

# SEO views
from .seo_views import robots_txt, custom_sitemap

__all__ = [
    'HomeView', 
    'AboutView', 
    'ContactView',
    'CategoryListView',
    'CategoryDetailView',
    'TagListView',
    'TagDetailView',
    'custom_404_view',
    'custom_500_view',
    'robots_txt', 
    'custom_sitemap'
]
