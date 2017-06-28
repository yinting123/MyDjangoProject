# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.template import loader, Context, Template
from django.http import HttpResponse

# Create your views here.

class Person(object):
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex

    def say(self):
        return "hello, i'am ",self.name

"""
    三步走：
    1.创建模板，载入模板
    2.创建参数对象
    3.对模板传入参数进行渲染
"""
def index(request):
    user = Person("liuhua",23,'female')
    return render_to_response("index.html",user)

def index1(request):
    t = Template('<h1>hello {{uname}}</h1>')
    c = Context({'uname':'helen'})
    return HttpResponse(t.render(c))

def index2(request):
    t = loader.get_template("index.html")
    c = Context()
    return HttpResponse(t.render())