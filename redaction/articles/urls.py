from django.urls import path

from articles.views import Create_article, Get_list_of_written_articles, Article_Page, pdf_view, pdf_view_article, Publish_the_article
from problems.views import List_of_problem
from main.views import List_view
app_name = 'articles'
urlpatterns = [
    path("list_published_articles", List_view.as_view(), name= 'list_published_articles'),
    path("list_articles", Get_list_of_written_articles.as_view(), name = 'list_articles'),
    path("create_new_article",Create_article.as_view(), name = 'create_new_article'),
    # path("create_new_article/<int:pk>",Create_article.as_view(), name = 'create_new_article')
    path("list_articles/articles/<int:pk>", Article_Page.as_view(), name = 'article_info'),
    path("list_articles/article/<int:pk>/problems", List_of_problem.as_view(), name = 'list_of_problems'),
    path("list_articles/article/<int:pk>/content", pdf_view, name = 'article_content'),
    path("list_articles/article/<int:pk>/review", pdf_view_article, name = 'article_review'),
     path("list_articles/article/<int:pk>/publish", Publish_the_article.as_view(), name = 'publish'),
    
]