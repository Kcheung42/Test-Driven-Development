# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# TODO: every post request creates empty list. Fix this
@csrf_exempt
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    return render(request, 'home.html')
