from django.urls import path

from . import views

urlpatterns = [
    path("send/", views.send, name="send"),
    path("retrieve/", views.retrieve, name="retrieve"),
    path("delete/", views.delete, name="delete"),
    path("device/", views.device, name="device"),
    path("getall/", views.getall, name="getall"),
]