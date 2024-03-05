from django import forms
from articles.models import Article
from users.models import User
from problems.models import Problem
class NewProblem(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['text']
        exclude = ['article', 'redactor']