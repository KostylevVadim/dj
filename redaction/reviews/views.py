from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View
from articles.models import Article

from reviews.forms import NewReview
from reviews.models import Review


# Create your views here.
class List_of_articles(ListView):
    template_name = 'reviews/list_articles.html'
    model = Article
    def get_context_data(self, **kwargs):
        # ids = []
        # q11 = Article.objects.values("title").annotate(Max("id"), Max("date"))
        # for q in q11:
        #     print(q)
        # res = []
        # for q in q11:
        #     res += Article.objects.filter(redactor = self.request.user, id = q['id__max'], status = 'RV1')
        # print(res)
        qs = Article.objects.filter(reviewer = self.request.user, status = 'RV1')
        # for q in qs:
        #     print(q.__dict__)
        
        return {'title': 'Написаные статьи', 'articles': qs}



class Create_review(View):
    template_name = 'reviews/create_review.html'
    def post(self, request, pk):
        form = NewReview(request.POST, request.FILES)
        
        form.instance.article = Article.objects.filter(id = pk)[0]
        # print(form.instance.article, pk, Article.objects.filter(id = pk))
        form.instance.reviewer = request.user
        # print(form.__dict__)
        if form.is_valid():
            form.save()
            
            return redirect('reviews:list_articles')
        return render(request, 'reviews/create_review.html', {'title': 'Добавление ревью', 'form': form})
    def get(self, request,pk):
        form = NewReview()
        return render(request, 'reviews/create_review.html', {'title': 'Добавление ревью', 'form': form})


class List_of_reviews(View):
    def get(self, request, pk):
        art = Article.objects.filter(id = pk)
        review = Review.objects.filter(article = pk)[-1]
        context = {
            'article': art,
            'review': review
        }
        return render(request, '')
    

class Agree_article(View):
    def get(self, request, pk):
        art = Article.objects.filter(id = pk)
        reviews = Review.objects.filter(article = pk)
        # problems = problems
        if len(art) == 0:
            return render(request, 'reviews/fail.html', {'title':'Ошибка','fail': 'Нет такой статьи'})
        if len(reviews) == 0:
            return render(request, 'reviews/fail.html', {'title':'Ошибка','fail': 'Нет рецензий'})
        art[0].status = 'AG1'
        art[0].save()
        return  HttpResponseRedirect(reverse('index'))