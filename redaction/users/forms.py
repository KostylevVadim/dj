from django import forms
from users.models import User
from django.contrib.auth.forms import UserCreationForm
 
class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 
