from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.health_views import HealthCheckView, ReadinessCheckView, LivenessCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🩺 Health Checks (for Docker/Kubernetes monitoring)
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('health/ready/', ReadinessCheckView.as_view(), name='readiness_check'),
    path('health/live/', LivenessCheckView.as_view(), name='liveness_check'),
    
    # Основные страницы
    path('', include('core.urls')),
    
    # Аутентификация (оставляем стандартный путь)
    path('accounts/', include('allauth.urls')),
    # Профиль пользователя (новый путь)
    path('profile/', include('accounts.urls')),
    
    # Контент
    path('stories/', include('stories.urls')),
    path('books/', include('books.urls')),
    path('audio/', include('audio.urls')),
    path('fairy-tales/', include('fairy_tales.urls')),
    
    # Коммерция
    path('shop/', include('shop.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    
    # Аналитика (если есть)
    path('analytics/', include('analytics.urls')),
]

# PWA и SEO функциональность - добавляем осторожно
try:
    from django.contrib.sitemaps.views import sitemap
    from core.views.seo_views import robots_txt
    from core.seo.sitemaps import sitemaps
    
    urlpatterns += [
        path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
        path('robots.txt', robots_txt, name='robots_txt'),
    ]
except ImportError:
    pass

try:
    from pwa.views import service_worker_view
    urlpatterns += [
        path('pwa/', include('pwa.urls')),
        path('sw.js', service_worker_view, name='service_worker'),
    ]
except ImportError:
    pass

# Для разработки - обслуживание медиа файлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
