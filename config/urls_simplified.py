from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
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
    
    # Временно отключаем проблемные URL
    # path('analytics/', include('analytics.urls')),
    # path('pwa/', include('pwa.urls')),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # path('robots.txt', robots_txt, name='robots_txt'),
    # path('sw.js', service_worker_view, name='service_worker'),
]

# Для разработки - обслуживание медиа файлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
