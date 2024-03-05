from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.views.generic import TemplateView
from problems.models import Problem
from articles.models import Article
from problems.forms import NewProblem
from django.db.models import Max
from django.http import HttpResponseRedirect
from typing import Any
from users.models import User
# Create your views here.
class List_of_articles(TemplateView):
    template_name = 'problems/list_articles.html'
    def get_context_data(self, **kwargs: Any):
        # ids = []
        # q11 = Article.objects.values("title").annotate(Max("id"), Max("date"))
        # for q in q11:
        #     print(q)
        # res = []
        # for q in q11:
        #     res += Article.objects.filter(redactor = self.request.user, id = q['id__max'], status = 'RD1')
        # print(res)
        qs = Article.objects.filter(redactor = self.request.user, status = 'RD1')
        # for q in qs:
        #     print(q.__dict__)
        
        return {'title': 'Написаные статьи', 'articles': qs}

class Create_problem(View):
    template_name = 'problems/create_problem.html'
    def post(self, request, pk):
        form = NewProblem(request.POST, request.FILES)
        
        form.instance.article = Article.objects.filter(id = pk)[0]
        # print(form.instance.article, pk, Article.objects.filter(id = pk))
        form.instance.redactor = request.user
        # print(form.__dict__)
        if form.is_valid():
            form.save()
            
            return redirect('problems:list_of_articles')
        return render(request, 'problems/create_problem.html', {'title': 'Добавление проблемы', 'form': form})
    def get(self, request,pk):
        form = NewProblem()
        return render(request, 'problems/create_problem.html', {'title': 'Добавление проблемы', 'form': form})

class List_of_problem(TemplateView):
    template_name = 'problems/list_of_problems.html'
    def get_context_data(self, pk,**kwargs: Any) -> dict[str, Any]:
        qs = Problem.objects.filter(article_id = pk)
        return {'title':'Список ошибок, полученных от редактора', 'problems' : qs}
    # def get(self, request,pk):
        
    #     return render(request, 'problems/create_problem.html', {'title': 'Добавление проблемы', 'form': form})

class Send_to_reviewer(View):
    def get(self, request, pk):
        # print('Here')
        art = Article.objects.filter(id = pk)[0]
        art.send_to_reviewer()
        problems = Problem.objects.filter(article = art)
        problems.delete()
        redactors = User.objects.filter(role = 'Reviewer').order_by('?')[0]
        art.reviewer = redactors
        art.save()
        return  HttpResponseRedirect(reverse('problems:list_of_articles'))

