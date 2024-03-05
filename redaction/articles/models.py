from django.db import models
from users.models import User
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator

# Create your models here.
class Article(models.Model):
    AUTHOR_READS = 'A1'
    REDACTOR_READS = 'RD1'
    REVIEWER_READS = 'RV1'
    AGREED = 'AG1'
    PUBLISHED = 'PU'
    ROLE = [
        (AUTHOR_READS, 'A'),
        (REDACTOR_READS, 'RD'),
        (REVIEWER_READS, 'RV'),
        (PUBLISHED, 'PU'),
        (AGREED,'AG1')
    ]
    path = models.FileField(upload_to='articles', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    date = models.DateField(default=now)
    title = models.CharField(max_length= 128)
    author = models.ForeignKey(to = User, null=True, on_delete = models.SET_NULL)
    status = models.CharField(max_length = 3, blank = True, default = REDACTOR_READS)
    # previous_version = models.OneToOneField(to = "self", related_name='previous', null = True,on_delete = models.SET_NULL)
    redactor = models.ForeignKey(to = User, related_name ="article_redactor", null=True, on_delete = models.SET_NULL)
    reviewer = models.ForeignKey(to = User, related_name ="article_reviewer", null=True, on_delete = models.SET_NULL)


    def send_to_author(self):
        try:
            self.status = self.AUTHOR_READS
        except:
            return 'Невозможно отправить автору'
        else:
            return 'Отправлено автору'
    def send_to_redactor(self):
        try:
            self.status = self.REDACTOR_READS
        except:
            return 'Невозможно отправить редактору'
        else:
            return 'Отправлено редактору'
    def send_to_reviewer(self):
        try:
            self.status = self.REVIEWER_READS
        except:
            return 'Невозможно отправить рецензенту'
        else:
            return 'Отправлено рецензенту'
    
    # def send_to_publish(self):
    #     prec_article = 
    

