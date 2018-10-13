#coding:utf-8
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import UUIDUser

# User: create
class UUIDUserForm(forms.ModelForm):
    class Meta:
        model = UUIDUser
        fields = ('username','first_name', 'last_name', 'password', 'email')
        labels = {
        'first_name': 'Nome',
        'last_name': 'Sobrenome',
        'username': 'Username',
        'email': 'E-mail',
        'password': 'Senha',
    }
        widgets={
            'password': forms.PasswordInput()
}


