from django import forms
from articles.models import Article
from users.models import User
from reviews.models import Review
class NewReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['path']
        exclude = ['article', 'reviewer']