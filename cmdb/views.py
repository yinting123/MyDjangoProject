# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.

def index(request):
     # return HttpResponse("hello world")
     if request.method == "post":
          user = request.POST.get("user")
          pwd = request.POST.get("password")
     return render(request,"index.html")

def result(request):
    if request.method == "POST":
        if request.POST.get("user") == "ting.yin" and \
            request.POST.get("password") == "123456":
            return render(request,"ShowResult.html")
        else:
            return render(request,"error.html")

    return render(request,"showResult.html")

def error(request):
    return render(request,"error.html")

def majia(request):
    return render(request, "MajiaCenterPrice/majiaInput.html")

def center_price(request):
    return render(request, "MajiaCenterPrice/center-price.html")

def process_majia(request):
    if request.method == "POST":
        emhotel = request.POST.get("elong_mhotel")
        cmhotel = request.POST.get("ctrip_mhotel")
        qmhotel = request.POST.get("qunar_mhotel")
        ci = request.POST.get("check_in")
        co = request.POST.get("check_out")
        settlement = request.POST.get("settlement")
        breakfast = request.POST.get("breakfast")
        return render(request,"ShowResult.html")