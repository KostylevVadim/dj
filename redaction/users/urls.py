from django.urls import path
from users.views import login_user, logout_from, SignUpView, UpdateProfile, ShowProfilePageView
from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'
urlpatterns = [
    path("login", login_user, name = 'login'),
    path("register", SignUpView.as_view(), name = 'register'),
    path("logout", logout_from, name = 'logout'),
    path("profile/<int:pk>", ShowProfilePageView.as_view(), name = 'profile'),
    path("update_profile/<int:pk>", UpdateProfile.as_view(), name = 'update_profile'),

    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

