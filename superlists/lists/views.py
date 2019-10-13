# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    context = {
        'items' : items
    }
    return render(request, 'list.djhtml', context)

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world')
