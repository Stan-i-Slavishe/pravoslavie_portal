from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Каталог и товары
    path('', views.product_list_view, name='catalog'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    
    # Корзина
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/count/', views.get_cart_count, name='cart_count'),
    
    # Оформление заказа
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/<uuid:order_id>/', views.payment_view, name='payment'),
    path('payment-success/<uuid:order_id>/', views.payment_success_view, name='payment_success'),
    
    # Заказы и покупки
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('order/<uuid:order_id>/', views.order_detail_view, name='order_detail'),
    path('my-purchases/', views.my_purchases_view, name='my_purchases'),
    path('download/<int:order_item_id>/', views.download_product, name='download_product'),
    path('download-purchase/<int:purchase_id>/', views.download_purchase, name='download_purchase'),
    
    # Промокоды
    path('apply-discount/', views.apply_discount, name='apply_discount'),
    
    # Персонализированные сказки
    path('order-fairy-tale/<int:product_id>/', views.order_fairy_tale, name='order_fairy_tale'),
]
