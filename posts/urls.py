from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("videos/<str:video_path>/", views.video, name="videos"),
    path("images/<str:image_path>/", views.image, name="images")
]