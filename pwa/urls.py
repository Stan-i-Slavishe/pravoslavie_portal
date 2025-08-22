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
    
    # 🔔 Новые страницы настроек уведомлений
    path('notifications/settings/', views.notification_settings_page, name='notification_settings'),
    path('api/save-notification-settings/', views.save_notification_settings, name='save_notification_settings'),
    path('api/get-notification-settings/', views.get_notification_settings, name='get_notification_settings'),
    
    # 📅 API для православного календаря
    path('api/orthodox-calendar/today/', views.orthodox_calendar_today, name='orthodox_calendar_today'),
    path('api/orthodox-calendar/<int:year>/<int:month>/<int:day>/', views.orthodox_calendar_date, name='orthodox_calendar_date'),
    
    # 📅 Страницы православного календаря
    path('orthodox-calendar/', views.orthodox_calendar_page, name='orthodox_calendar'),
    path('daily-calendar/', views.daily_orthodox_page, name='daily_orthodox_calendar'),
    
    # 📅 API для ежедневной православной информации
    path('api/daily-orthodox/<int:year>/<int:month>/<int:day>/', views.daily_orthodox_info, name='daily_orthodox_info'),
    
    # 📅 API для календарного виджета
    path('api/calendar-month/<int:year>/<int:month>/', views.orthodox_calendar_month, name='orthodox_calendar_month'),
]
