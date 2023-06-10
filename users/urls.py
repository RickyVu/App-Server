from django.urls import path

from . import views

urlpatterns = [
    path('is_logged_in/', views.is_logged_in, name='is_logged_in'),
    path('login/', views.log_in, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.log_out, name='logout'),
    path('check_username/', views.check_username_available, name='check_username'),
    path('description/', views.description, name='description'),
    path('profile_picture/', views.profile_picture, name='profile_picture'),
    path('find_users/', views.find_users, name='find_users'),
    path('username/', views.username, name='username'),
    path('blacklist/', views.blacklist, name='blacklist'),
    path('follower/', views.follower, name='follower'),
    path('follow/', views.follow, name='follow'),
    path('change_username/', views.change_username, name='change_username'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_description/', views.change_description, name = 'change_description'),
    path('change_profile_picture/', views.change_profile_picture, name='change_profile_picture'),
    path('follower_count/', views.follower_count, name='follower_count'),
    path('follow_count/', views.follow_count, name='follow_count'),
    path('is_following/', views.is_following, name='is_following'),
    path('is_blacklisted/', views.is_blacklisted, name='is_blacklisted'),
    path('getall/', views.getall, name='getall'),
    path('test/', views.session_test, name="test"),
    path('reqlogin/', views.req_login, name='reqlogin')
]