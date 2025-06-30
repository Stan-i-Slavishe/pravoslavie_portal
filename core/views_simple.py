from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'core/home_simple.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        
        # Заглушка для настроек
        class DummySettings:
            site_name = "Православный портал"
            site_description = "Духовные рассказы, книги и аудио для современного человека"
        
        context['site_settings'] = DummySettings()
        context['story_categories'] = []
        context['book_categories'] = []
        context['audio_categories'] = []
        context['popular_tags'] = []
        
        return context