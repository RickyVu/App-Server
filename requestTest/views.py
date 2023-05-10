from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .utils import get_all_urls
from django.urls import get_resolver
from django.middleware import csrf

import copy
# Create your views here.
def get(request):
    csrf_token = request.session["csrf_token"] if request.session.get("csrf_token", None) else csrf.get_token(request)
    context = {'url_list': get_all_urls(), 'csrf_token': csrf_token}
    return render(request, 'get.html', context)

def post(request):
    print(request.session["csrf_token"] if request.session.get("csrf_token", None) else csrf.get_token(request))
    csrf_token = request.session["csrf_token"] if request.session.get("csrf_token", None) else csrf.get_token(request)
    context = {'url_list': get_all_urls(), 'generated_csrf_token': csrf_token}
    return render(request, 'post.html', context)