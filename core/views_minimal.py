from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Простые заглушки без обращения к базе данных
        class DummySettings:
            site_name = "Добрые истории"
            site_description = "Духовные рассказы, книги и аудио для современного человека"
        
        context['site_settings'] = DummySettings()
        context['story_categories'] = []
        context['book_categories'] = []
        context['audio_categories'] = []
        context['popular_tags'] = []
        
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О проекте'
        
        # Заглушка для настроек
        class DummySettings:
            site_name = "Добрые истории"
            site_description = "Духовные рассказы, книги и аудио для современного человека"
            contact_email = "info@dobrye-istorii.ru"
            contact_phone = "+7 (800) 123-45-67"
        
        context['site_settings'] = DummySettings()
        
        # Статистика для страницы о проекте
        context['total_stories'] = 150
        context['total_books'] = 300
        context['total_audio'] = 200
        context['total_users'] = 1500
        context['founding_year'] = 2020
        
        return context
