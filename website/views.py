# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
def website(request):
    return render(request, 'website/index_website.html')