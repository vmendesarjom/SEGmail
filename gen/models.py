# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.db import models

# CreateUpdateModel
# - - - - - - - - - - - - - - - - - - -
class CreateUpdateModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        abstract = True

# UUIDUser
# - - - - - - - - - - - - - - - - - - -
class UUIDUser(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groups = models.ManyToManyField(Group, blank=True, related_name="uuiduser_set", related_query_name="user")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="uuiduser_set", related_query_name="user")
    public = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

# Email
# - - - - - - - - - - - - - - - - - - -
class Email(models.Model):

    de_user = models.ForeignKey(UUIDUser, on_delete=models.CASCADE, related_name='usuarios')
    para_user = models.EmailField(max_length=255, null=False, blank=False)
    texto = models.TextField(null=True, blank=True)
    anexo = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')