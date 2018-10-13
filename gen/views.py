from django.shortcuts import render

from . import models
from .forms import UUIDUserForm

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
from base64 import b64encode, b64decode

import psycopg2, psycopg2.extras

# Base Template View
#----------------------
class BaseView(TemplateView):

    template_name = 'home.html'

# User Create View
#----------------------
class UserCreateView(CreateView):
    
    model = models.UUIDUser
    template_name = 'form.html'
    success_url = reverse_lazy('gen:login')
    form_class = UUIDUserForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(obj.password)
        obj.save()

        random_generator = Random.new().read
        key = RSA.generate(tamanho_chave, random_generator)
        private = key
        public = key.publickey()
        obj.public = public
        obj.save()
        db = psycopg2.connect("dbname=private user=postgres password=teste123 host=127.0.0.1")
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO private (id, chave) VALUES (%s, %s)", (str(self.request.user.pk), private))
        cur.close()
        db.close()

        return super(UserCreateView, self).form_valid(form)

# Email Create View
#----------------------
class EmailCreateView(CreateView):

    model = models.Email
    template_name = 'email.html'
    success_url = reverse_lazy('gen:home')
    fields = ['para_user', 'texto', 'anexo']

    def post(self, request):
        aux = dict(self.request.POST)
        print(aux)
        e = models.Email.objects.create(de_user=self.request.user)
        text = aux["texto"]
        anex = aux["anexo"]
        chave = models.UUIDUser.objects.filter(id=self.request.user).public
        if text != "":
            cipher = PKCS1_OAEP.new(chave)
            cipher.encrypt(text)
            e.texto = text
        e.save()

# Email List View
#----------------------
class EmailView(ListView):

    model = models.Email
    template_name = 'email-list.html'
    

    def get_context_data(self, **kwargs):
        object_list = []
        for obj in models.Email.objects.filter(para_user=self.request.user):
            object_list.append(obj)

        db = psycopg2.connect("dbname=private user=postgres password=teste123 host=127.0.0.1")
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        ex = ("FROM chave IMPORT * WHERE id=self.request.user")

        textd_list = []
        if object_list != "":
            for objc in object_list:
                text_d = cipher.decrypt(objc.text)
                text_d = text_d.rstrip(ex)
                textd_list.append(objc)
            kwargs['textd_list'] = textd_list

        return super(EmailView, self).get_context_data(**kwargs) 