from django.urls import include, path, re_path
from . import views
from django.views.generic import TemplateView
app_name = 'requestTest'
urlpatterns = [
    path('get/', views.get),
    path('post/', views.post),
]