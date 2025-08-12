from django.urls import path
from . import views

app_name = 'fairy_tales'

urlpatterns = [
    # Заглушка "Скоро"
    path('', views.coming_soon, name='list'),  # Оставляем name='list' для совместимости
    
    # AJAX для подписки на уведомления
    path('ajax/subscribe/', views.subscribe_notification, name='subscribe_notification'),
]

# БУДУЩИЕ URLs - РАЗКОММЕНТИРОВАТЬ ПРИ ЗАПУСКЕ СКАЗОК
"""
urlpatterns = [
    # Основные страницы
    path('', views.FairyTaleListView.as_view(), name='list'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    
    # Страницы сказок
    path('tale/<slug:slug>/', views.FairyTaleDetailView.as_view(), name='detail'),
    path('personalize/<slug:slug>/', views.PersonalizationOrderView.as_view(), name='personalize'),
    path('order-success/<uuid:order_id>/', views.OrderSuccessView.as_view(), name='order_success'),
    
    # Личный кабинет
    path('my-orders/', views.MyOrdersView.as_view(), name='my_orders'),
    path('my-favorites/', views.MyFavoritesView.as_view(), name='my_favorites'),
    
    # AJAX эндпоинты
    path('ajax/favorite/<int:template_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('ajax/review/<int:template_id>/', views.add_review, name='add_review'),
    path('ajax/preview/', views.preview_personalization, name='preview_personalization'),
    path('ajax/calculate-price/', views.calculate_price, name='calculate_price'),
]
"""
