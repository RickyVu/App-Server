from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.log_out, name='logout'),
    path('getall/', views.getall, name='getall'),
    path('test/', views.session_test, name="test"),
    path('reqlogin/', views.req_login, name='reqlogin')
]