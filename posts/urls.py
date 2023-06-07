from django.urls import path

from . import views

urlpatterns = [
    path("test/", views.test, name="index"),
    path("retrieve/", views.retrieve, name="retrieve"),
    path("post/", views.post, name="post"),
    path("like/", views.like, name="like"),
    path("favourite/", views.favourite, name="favourite"),
    #path("videos/<str:video_path>/", views.video, name="videos"),
    #path("images/<str:image_path>/", views.image, name="images")
]