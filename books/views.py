from django.views.generic import ListView, DetailView

class BookListView(ListView):
    template_name = 'books/list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        return []

class BookDetailView(DetailView):
    template_name = 'books/detail.html'
    context_object_name = 'book'
    
    def get_object(self):
        return None

class ArticleListView(ListView):
    template_name = 'books/articles.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        return []

class ArticleDetailView(DetailView):
    template_name = 'books/article_detail.html'
    context_object_name = 'article'
    
    def get_object(self):
        return None