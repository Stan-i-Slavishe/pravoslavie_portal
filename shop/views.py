from django.views.generic import TemplateView

class ShopView(TemplateView):
    template_name = 'shop/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Магазин'
        return context

class CartView(TemplateView):
    template_name = 'shop/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        return context

class CheckoutView(TemplateView):
    template_name = 'shop/checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        return context

class OrderHistoryView(TemplateView):
    template_name = 'shop/orders.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'История заказов'
        return context