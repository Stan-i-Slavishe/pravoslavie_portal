from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ShopView.as_view(), name='index'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/', views.OrderHistoryView.as_view(), name='orders'),
]