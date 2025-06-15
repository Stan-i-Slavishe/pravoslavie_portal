from django.views.generic import ListView, DetailView, TemplateView

class StoryListView(ListView):
    template_name = 'stories/list.html'
    context_object_name = 'stories'
    
    def get_queryset(self):
        # Пока возвращаем пустой список
        return []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Видео-рассказы'
        return context

class StoryDetailView(DetailView):
    template_name = 'stories/detail.html'
    context_object_name = 'story'
    
    def get_object(self):
        # Заглушка
        return None

class StoryCategoryView(ListView):
    template_name = 'stories/category.html'
    context_object_name = 'stories'
    
    def get_queryset(self):
        return []