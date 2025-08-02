# analytics/urls.py

from django.urls import path
from . import views
from . import production_views

app_name = 'analytics'

urlpatterns = [
    # ========== PRODUCTION ANALYTICS ==========
    # Основной endpoint для отслеживания событий
    path('track-event/', production_views.track_event, name='track_event'),
    
    # Дашборды для продакшена
    path('dashboard/', production_views.production_dashboard, name='dashboard'),
    path('real-time/', production_views.real_time_stats, name='real_time_stats'),
    path('export/', production_views.export_analytics, name='export_analytics'),
    
    # ========== LEGACY ENDPOINTS (для совместимости) ==========
    # Старые API (если где-то еще используются)
    path('track-purchase-intent/', views.track_purchase_intent, name='track_purchase_intent'),
    path('subscribe-notifications/', views.subscribe_notifications, name='subscribe_notifications'),
    path('api/stats/', views.api_stats, name='api_stats'),
    
    # Email подписки (публичные страницы)
    path('subscribe/', views.subscription_form, name='subscription_form'),
    path('subscribe/success/', views.subscription_success, name='subscription_success'),
    path('unsubscribe/<int:subscription_id>/', views.unsubscribe, name='unsubscribe'),
    
    # Управление email кампаниями (только для админов)
    path('email-campaigns/', views.email_campaigns, name='email_campaigns'),
]
