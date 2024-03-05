from django.urls import path

from problems.views import List_of_articles, Create_problem, Send_to_reviewer

app_name = 'problems'
urlpatterns = [
    path("list_of_articles", List_of_articles.as_view(), name = 'list_of_articles'),
    path("problem_of_article/<int:pk>",Create_problem.as_view(), name = 'problem'),
    path("send_to_reviewer/<int:pk>", Send_to_reviewer.as_view(), name = 'review')
    # path("create_new_article/<int:pk>",Create_article.as_view(), name = 'create_new_article')
    
]