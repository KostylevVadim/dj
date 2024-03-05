from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import LoginUserForm, RegistrationForm
# Create your views here.
import os
from os import listdir

from users.models import User
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.detail import DetailView

from redaction.settings import MEDIA_ROOT
def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            login(request, user)
            return redirect('/', permanent= True)
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'title': 'Вход','form': form})

class SignUpView(CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    form_class = RegistrationForm


def logout_from(request):
    logout(request)
    return redirect('/', permanent= True)

class ShowProfilePageView(DetailView):
    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, *args, **kwargs):
        users = User.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(User, id=self.kwargs['pk'])
        # print(page_user.__dict__)
        file_path = MEDIA_ROOT
        onlyfiles = [f for f in listdir(file_path)]
        # print(onlyfiles)
        context['page_user'] = page_user
        context['Username'] = page_user.username
        context['first_name'] = page_user.first_name
        context['last_name'] = page_user.last_name
        context['email'] = page_user.email
        context['title'] = page_user.title
        context['role'] = page_user.role
        context['image']= page_user.image
        
        return context


class UpdateProfile(UpdateView):
    model = User
    fields = ['username', 
              'first_name',
              'last_name'
              ,'title', 
              'image']
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title_of': 'Редактирование профиля',
    }
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        post = super().post(request, *args, **kwargs)
        # print(post.__dict__)
        # print(request.__dict__)
        return post



