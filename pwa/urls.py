# PWA URLs for Православный портал

from django.urls import path
from . import views

app_name = 'pwa'

urlpatterns = [
    # Основные PWA файлы
    path('manifest.json', views.manifest_view, name='manifest'),
    path('sw.js', views.service_worker_view, name='service_worker'),
    
    # Офлайн страницы
    path('offline/', views.OfflineView.as_view(), name='offline'),
    
    # Push-уведомления
    path('push/subscribe/', views.push_subscribe, name='push_subscribe'),
    
    # Синхронизация данных
    path('sync/playlists/', views.sync_playlists, name='sync_playlists'),
    path('sync/favorites/', views.sync_favorites, name='sync_favorites'),
    path('sync/cart/', views.sync_cart, name='sync_cart'),
    
    # API
    path('api/orthodoxy-calendar/today/', views.orthodoxy_calendar_today, name='orthodoxy_calendar_today'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('ping/', views.ping, name='ping'),
    
    # 🔔 Тестирование push-уведомлений (только для разработки)
    path('push/test/', views.push_test_page, name='push_test'),
]
