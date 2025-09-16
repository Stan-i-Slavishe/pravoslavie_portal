from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.health_views import HealthCheckView, ReadinessCheckView, LivenessCheckView

# 📊 Мониторинг - импорт views
try:
    from core.monitoring_views import (
        monitoring_dashboard, monitoring_api_system, monitoring_api_database,
        monitoring_api_cache, monitoring_api_application, monitoring_api_logs,
        monitoring_api_alerts, health_check, health_check_detailed
    )
    MONITORING_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Ошибка импорта мониторинга: {e}")
    MONITORING_AVAILABLE = False

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🩺 Health Checks (for Docker/Kubernetes monitoring)
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('health/ready/', ReadinessCheckView.as_view(), name='readiness_check'),
    path('health/live/', LivenessCheckView.as_view(), name='liveness_check'),
    
    # 👨‍💻 Основные страницы
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

# 📊 Условное добавление URL мониторинга
if MONITORING_AVAILABLE:
    monitoring_urls = [
        path('admin/monitoring/dashboard/', monitoring_dashboard, name='monitoring_dashboard'),
        path('admin/monitoring/api/system/', monitoring_api_system, name='monitoring_api_system'),
        path('admin/monitoring/api/database/', monitoring_api_database, name='monitoring_api_database'),
        path('admin/monitoring/api/cache/', monitoring_api_cache, name='monitoring_api_cache'),
        path('admin/monitoring/api/application/', monitoring_api_application, name='monitoring_api_application'),
        path('admin/monitoring/api/logs/', monitoring_api_logs, name='monitoring_api_logs'),
        path('admin/monitoring/api/alerts/', monitoring_api_alerts, name='monitoring_api_alerts'),
        path('health/simple/', health_check, name='health_check_simple'),
        path('health/detailed/', health_check_detailed, name='health_check_detailed'),
    ]
    urlpatterns = monitoring_urls + urlpatterns
    print("✅ Мониторинг URL добавлены")
else:
    print("⚠️ Мониторинг недоступен, используйте /test/monitoring/")

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
