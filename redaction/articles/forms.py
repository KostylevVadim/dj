from django import forms
from articles.models import Article
from users.models import User
    # path = models.FileField(upload_to='articles')
    # date = models.DateField(default=now)
    # title = models.CharField(max_length= 128)
    # author = models.ForeignKey(to = User, null=True, on_delete = models.SET_NULL)
    # status = models.CharField(max_length = 2, blank = True, default = REDACTOR_READS)
class NewArticle(forms.Form):
    def is_valid(self) -> bool:
        redactor = User.objects.filter(role = 'Redactor').order_by('?')[0]
        print(redactor, 'isvalid')
        # con = Article_Redactor()
        # con.redactor = redactor
        # con.article = form.instance.id
        # con.save()
        return super().is_valid()

    
    class Meta:
        model = Article
        fields = ['title','path']

    

