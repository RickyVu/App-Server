from django.urls import path

from . import views

urlpatterns = [
    path("retrieve/", views.retrieve, name="retrieve"),
    path("post/", views.post, name="post"),
    path("like/", views.like, name="like"),
    path("favourite/", views.favourite, name="favourite"),
    path("favourite_count/", views.favourite_count, name="favourite_count"),
    path("comment/", views.comment, name="comment"),
    #path("videos/<str:video_path>/", views.video, name="videos"),
    #path("images/<str:image_path>/", views.image, name="images")
]