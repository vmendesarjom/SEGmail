from __future__ import unicode_literals

from django.urls import include, path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views as gen

app_name = "gen"

urlpatterns = [

    path('', gen.BaseView.as_view(), name='home'),

    # Login
    path('login/', auth_views.LoginView.as_view(template_name='auth.html'), name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #Cadastro de usuario
    path('usuarios/novo/', gen.UserCreateView.as_view(), name='user-create'),

    path('email/novo/', gen.EmailCreateView.as_view(), name='email'),
    path('email/entrada/', gen.EmailView.as_view(), name='email-list'),
]