from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return HttpResponse("Hello, world. You're at the posts index.")

def video(request, video_path):
    video_url = f'http://localhost/videos/{video_path}'
    return HttpResponseRedirect(video_url)

def image(request, image_path):
    image_url = f'http://localhost/images/{image_path}'
    return HttpResponseRedirect(image_url)
