# analytics/urls.py

from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # API для отслеживания
    path('track-purchase-intent/', views.track_purchase_intent, name='track_purchase_intent'),
    path('subscribe-notifications/', views.subscribe_notifications, name='subscribe_notifications'),
    path('api/stats/', views.api_stats, name='api_stats'),
    
    # Дашборд аналитики
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    
    # Email подписки (публичные страницы)
    path('subscribe/', views.subscription_form, name='subscription_form'),
    path('subscribe/success/', views.subscription_success, name='subscription_success'),
    path('unsubscribe/<int:subscription_id>/', views.unsubscribe, name='unsubscribe'),
    
    # Управление email кампаниями (только для админов)
    path('email-campaigns/', views.email_campaigns, name='email_campaigns'),
]
