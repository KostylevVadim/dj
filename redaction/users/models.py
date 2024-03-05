from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator
# Create your models here.



class User(AbstractUser):
    AUTHOR = 'Author'
    REDACTOR = 'Redactor'
    REVIEWER = 'Reviewer'
    ROLE = [
        (AUTHOR, 'A'),
        (REDACTOR, 'RD'),
        (REVIEWER, 'RV'),
    ]
    image = models.ImageField(upload_to='images', blank=True, default= 'default.png', validators=[FileExtensionValidator(allowed_extensions=['png'])])
    title = models.TextField(max_length = 500, blank = True)
    role = models.CharField(max_length = 8, blank = True, default = AUTHOR)
    
    def is_author(self):
        return self.role in {self.AUTHOR}
    def is_redactor(self):
        return self.role in {self.REDACTOR}
    def is_reviewer(self):
        return self.role in {self.REVIEWER}



