from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from articles.models import Article
# Create your views here.

def index(request):
    return render(request,'main/home.html')

class IndexView(TemplateView):
    template_name = 'main/home.html'
    title = 'Редакция'
    def get_context_data(self, **kwargs):
        return {'title': self.title}

class List_view(View):
    def get(self, request):
        qs = Article.objects.filter(status = 'PUB')
        return render(request, 'main/list_articles.html', {'title':'Опубликованные статьи', 'articles': qs})


