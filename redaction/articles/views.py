from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, View
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from articles.models import Article
from users.models import User 
from articles.forms import NewArticle
from problems.models import Problem
import os
from redaction.settings import MEDIA_ROOT
from django.http import FileResponse
from reviews.models import Review
# Create your views here.

class Create_article(CreateView):
    success_url = reverse_lazy('index')
    template_name = 'articles/create_new_article.html'
    model = Article
    fields = ['title','path']
    def form_valid(self, form: NewArticle) -> HttpResponse:
        # print(self.request)
        qs = Article.objects.filter(title = form.instance.title)
        if len(qs) > 0:
            art = qs[0]
            # print('here')
            if qs[0].status not in ['RV1', 'PUB', 'AG1']:
                art.path = form.instance.path
                art.save()
                probs = Problem.objects.filter(article = art.id)
                probs.delete()
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(reverse('index'))
        else:
            form.instance.author = self.request.user
            # print(self.request.user, User.objects.filter(role = 'Redactor'))
            # for i in range(10):
            #     print(User.objects.filter(role = 'Redactor').order_by('?')[0])
            redactors = User.objects.filter(role = 'Redactor').order_by('?')[0]
            form.instance.redactor = redactors
            return super().form_valid(form)


    def post(self, request, *args: str, **kwargs: Any) -> HttpResponse:
        post = super().post(request, *args, **kwargs)
        print(post.__dict__)
        # print(request.__dict__)
        return post

class Article_Page(TemplateView):
    template_name = 'articles/article.html'
    def get_context_data(self, pk, **kwargs: Any):
        qs = Article.objects.filter(id = pk)
        
        return {'title': 'Статья', 'title': qs[0].title, 'date': qs[0].date,
                'author': qs[0].author, 'id': qs[0].id, 'status': qs[0].status} 

def pdf_view(request,pk):
    
    article = Article.objects.filter(id = pk)
    if len(article) == 0:
        return render(request,'articles/fail.html', {'title':'Ошибка','fail': 'Статья отсутствует'})
    path = article[0].path
    filepath = os.path.join(MEDIA_ROOT, str(path))
    print(filepath)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

def pdf_view_article(request,pk):
    print('here')
    article = Review.objects.filter(article = pk)
    print(article,len(article))
    if len(article) == 0:
        return render(request, 'articles/fail.html',{'title': 'Ошибка', 'fail': 'Рецензии пока нет'})
    path = article[0].path
    filepath = os.path.join(MEDIA_ROOT, str(path))
    # print(article)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
         

class Get_list_of_written_articles(TemplateView):
    template_name = 'articles/list_articles.html'
    def get_context_data(self, **kwargs: Any):
        qs = Article.objects.filter(author = self.request.user)
        return {'title': 'Написаные статьи', 'articles': qs} 


class Publish_the_article(View):
    def get(self, request, pk):
        art = Article.objects.filter(id = pk, status = 'AG1')[0]
        if len(Article.objects.filter(id = pk, status = 'AG1')) == 0:
            return render(request, 'articles/fail.html',{'title': 'Ошибка', 'fail': 'Такая статья еще не готова к пуюликации'})
        art.status = 'PUB'
        art.save()
        return redirect('articles:list_articles')


class List_after_search(View):
    def get(self, request):
        return render(request, 'main/search_result.html', {'title': 'Результат поиска'})
    
    def post(self, request, search_string):
        arts = Article.objects.filter(title__contains = search_string)
        return render(request, 'main/search_result.html', {'title': 'Результат поиска', 'context': arts})
        