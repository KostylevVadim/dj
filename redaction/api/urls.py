from django.urls import path, include
from api.views import Article_list_api, Article_list_api_author, Article_list_api_reviewer, Article_list_api_redactor, Create_article
from rest_framework import routers
import rest_framework
from django.contrib.auth import views
app_name = 'api'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='api/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("list-published-articles-api", Article_list_api.as_view(), name= 'list_published_articles'),
    path("list-author-articles-api", Article_list_api_author.as_view(), name= 'list_author_articles'),
    path("list-rev-articles-api", Article_list_api_reviewer.as_view(), name= 'list_rev_articles'),
    path("list-red-articles-api", Article_list_api_redactor.as_view(), name= 'list_red_articles'),
    path("create-article-api", Create_article.as_view(), name = 'create_article')
    ]