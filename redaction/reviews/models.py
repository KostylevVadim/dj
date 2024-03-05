from django.db import models
from articles.models import Article
from users.models import User
from django.core.validators import FileExtensionValidator
# Create your models here.
class Review(models.Model):
    path = models.FileField(upload_to='reviews', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    article = models.ForeignKey(to = Article, related_name = "article",null = True, on_delete = models.SET_NULL)
    reviewer = models.ForeignKey(to = User, related_name = "reviewer", null = True, on_delete = models.SET_NULL)

