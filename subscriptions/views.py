from django.views.generic import TemplateView

class SubscriptionPlansView(TemplateView):
    template_name = 'subscriptions/plans.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тарифы подписки'
        return context

class SubscribeView(TemplateView):
    template_name = 'subscriptions/subscribe.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление подписки'
        return context

class ManageSubscriptionView(TemplateView):
    template_name = 'subscriptions/manage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Управление подпиской'
        return context