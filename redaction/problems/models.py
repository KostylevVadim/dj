from django.db import models
from articles.models import Article
from users.models import User
# Create your models here.

class Problem(models.Model):
    text = models.TextField(max_length = 10000,blank = False, null = False)
    article = models.ForeignKey(to = Article, on_delete = models.CASCADE)
    redactor = models.ForeignKey(to = User, on_delete = models.CASCADE)