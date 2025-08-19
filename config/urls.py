from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.views.seo_views import robots_txt
from core.seo.sitemaps import sitemaps
from pwa.views import service_worker_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # SEO маршруты
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    
    # Основные страницы
    path('', include('core.urls')),
    
    # Аутентификация
    path('accounts/', include('allauth.urls')),
    
    # Профиль пользователя
    path('profile/', include('accounts.urls')),
    
    # Контент
    path('stories/', include('stories.urls')),
    path('books/', include('books.urls')),
    path('audio/', include('audio.urls')),
    path('fairy-tales/', include('fairy_tales.urls')),  # Терапевтические сказки
    
    # Коммерция
    path('shop/', include('shop.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    
    # Аналитика
    path('analytics/', include('analytics.urls')),
    
    # 🚀 PWA функциональность (ИСПРАВЛЕНО)
    path('pwa/', include('pwa.urls')),
    
    # Service Worker из корня для правильного scope
    path('sw.js', service_worker_view, name='service_worker'),
]

# Для разработки - обслуживание медиа файлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
