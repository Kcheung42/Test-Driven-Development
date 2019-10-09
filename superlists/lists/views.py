# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from lists.models import Item
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# TODO: every post request creates empty list. Fix this
@csrf_exempt
def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
    else:
        new_item_text = ''

    context = {
        'new_item_text': new_item_text,
    }
    return render(request, 'home.html', context)
