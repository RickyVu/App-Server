from django.urls import path

from . import views

urlpatterns = [
    path("send/", views.upload, name="send"),
    path("retrieve/", views.take, name="retrieve"),
    path("delete/", views.delete, name="delete"),
    path("device/", views.device, name="device"),
]