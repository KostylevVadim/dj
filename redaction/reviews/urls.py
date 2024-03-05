from django.urls import path
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from reviews.views import List_of_articles, Create_review, Agree_article
app_name = 'reviews'

urlpatterns = [
    path("list_articles", List_of_articles.as_view(), name = 'list_articles'),
    path("<int:pk>/create_review", Create_review.as_view(), name = 'create_review'),
    path("<int:pk>/agree_article", Agree_article.as_view(), name = 'agree_article')
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)