# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class users(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=15)
    password = models.BinaryField(max_length=100)
    createDate = models.DateField()
    operTime = models.DateField()
