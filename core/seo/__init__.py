# core/seo/__init__.py
"""
SEO utilities for the Orthodox Portal
"""

from .meta_tags import SEOManager, page_meta
from .sitemaps import generate_sitemap
from .schema_org import get_schema_data

__all__ = ['SEOManager', 'page_meta', 'generate_sitemap', 'get_schema_data']
