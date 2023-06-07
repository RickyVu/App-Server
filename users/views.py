import os
import uuid
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user
from django.middleware import csrf
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.utils import IntegrityError
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from serializers import ImageSerializer
from PIL import Image as Img
from media.models import Image
from io import BytesIO
from . import models
import json

def log_in(request):
    if request.method == 'POST':
        # Get the username and password from the request
        try:
            # Get the JSON data from the request body
            data = json.loads(request.body)

            username = data['username']
            password = data['password']
            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                #csrf_token = csrf.get_token(request)
                #request.session['csrf_token'] = csrf_token
                return JsonResponse({'success': True, 'message': 'login successful'})
            else:
                # Handle invalid login credentials
                return JsonResponse({'success': False, 'message': 'invalid login credentials'})
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success': False, 'message': 'invalid request'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

def signup(request):
    if request.method == 'POST':
        # Get the username and password from the request
        try:
            # Get the JSON data from the request body
            data = json.loads(request.body)

            username = data['username']
            password = data['password']

            if username==None or password==None:
                return JsonResponse({'success': False, "message": 'fields cannot be empty'})
            try:
                user = models.MyUser.objects.create_user(username=username, password=password)
                user.save()
                return JsonResponse({'success': True, 'message': 'signup successful'})
            except IntegrityError:
                return JsonResponse({'success': False, "message": 'clashing unique fields'})

        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success': False, 'message': 'invalid request'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@login_required
def log_out(request):
    logout(request)
    return JsonResponse({'message': 'logout successful'})

def check_username_available(request):
    if request.method == 'POST':

        try:
            # Get the JSON data from the request body
            data = json.loads(request.body)

            username = data['username']

            # Check if a user with the specified username already exists
            if models.MyUser.objects.filter(username=username).exists():
                return JsonResponse({'available':False})
            else:
                return JsonResponse({'available':True})
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'message': 'invalid request'}, status=400)
    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)

@login_required
def description(request):
    if request.method == 'GET':
        return JsonResponse({'description':request.user.description})
    elif request.method == 'PATCH':
        try:
            # Get the JSON data from the request body
            data = json.loads(request.body)

            description = data['description']

            user = request.user
            user.description = description
            user.save()
            return JsonResponse({'success': True, 'message': 'set description successful'})
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success':False, 'message': 'invalid request'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

def profile_picture(request):
    if request.method == 'GET':
        user_id = request.GET.get('id')
        if user_id:
            user = models.MyUser.objects.get(id=int(user_id))
        else:
            user = request.user
        #image_path = os.path.join(settings.BASE_DIR, "assets", "images", user.profile_picture.get_url())
        image_path = user.profile_picture.get_url()
        return HttpResponseRedirect(image_path)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

def find_users(request):
    if request.method == "GET":
        part_username = request.GET.get("username")
        if part_username:
            possible_users = models.MyUser.objects.exclude(id=request.user.id).filter(username__contains=part_username)[:30]
            possible_result = [{'user_id': user.id, 'username': user.username, 'profile_picture': user.profile_picture.get_url()} for user in possible_users]
            return JsonResponse({'success': True, 'message': possible_result})
        else:
            return JsonResponse({'success': False, 'message': 'get request requires username or part of username as input'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@login_required
def change_username(request):
    if request.method == "POST":
        try:
            # Get the JSON data from the request body
            data = json.loads(request.body)
            new_username = data['username']

            user = request.user
            user.username = new_username
            user.save()

            return JsonResponse({'success': True, 'message': 'change username successful'})
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success':False, 'message': 'invalid request'}, status=400)
        except (django.db.IntegrityError) as e:
            return JsonResponse({'success':False, 'message': 'username occupied'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@login_required
def change_password(request):
    if request.method == "POST":
        try:
            # Get the JSON data from the request body
            data = json.loads(request.body)
            old_password = data['old']
            new_password = data['new']

            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return JsonResponse({'success': True, 'message': 'set password successful'})
            else:
                return JsonResponse({'success': False, 'message': 'old password error'})


        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'success':False, 'message': 'invalid request'}, status=400)
        except ValueError:
            return JsonResponse({'success':False, 'message': 'value error'}, status=400)
        except TypeError:
            return JsonResponse({'success':False, 'message': 'type error'}, status=400)
        except (RuntimeError, AttributeError):
            return JsonResponse({'success':False, 'message': 'internal error'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@login_required
def change_description(request):
    if request.method == "POST":
        try:
            user = request.user
            data = json.loads(request.body)
            new_description = data["description"]

            user.description = new_description
            user.save()
            return JsonResponse({'success':True, 'message': 'change description successful'})
        except:
            return JsonResponse({'success': False, 'message': 'error'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status = 405)

@login_required
def change_profile_picture(request):
    if request.method == "POST":
        try:
            user = request.user
            new_profile_picture_data = request.FILES.get('image')

            image_model = Image()
            image_model.save()
            user.profile_picture = image_model
            user.save()

            image_path = os.path.join(settings.BASE_DIR, "assets", "images", image_model.get_file_name())
            image = Img.open(new_profile_picture_data)

            image.save(image_path, 'JPEG', quality=70)


            return JsonResponse({'success': True, 'message': 'change profile picture successful', "Image ID:": image_model.id})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'success':False, 'message': 'invalid request'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)
# ______________________TESTS_______________________
def getall(request):
    if (len(list(models.MyUser.objects.all().values())))==0:
        return JsonResponse({"EMPTY": "NULL"})
    else:
        result = dict()
        for obj, values in zip(models.MyUser.objects.all(), models.MyUser.objects.all().values()):
            result[str(obj)] = values
        return JsonResponse(result)

def session_test(request):
    csrf_token = request.session.get('csrf_token', '')
    #session_data = cache.get(session_key)
    #print(session_data)
    print(request.session, request.session.session_key)#dir(request.session))
    if request.user.is_authenticated:
        # user is logged in
        if hasattr(request.session, 'session_key'):
            return JsonResponse({'logged_in':True, 'csrf_token': csrf_token, 'session_key': request.session.session_key, 'message': 'logged in'})
        else:
            return JsonResponse({'logged_in':False, 'csrf_token': csrf_token, 'session_key': request.session.session_key, 'message': 'no session key'})
    else:
        return JsonResponse({'logged_in':False, 'csrf_token': csrf_token, 'session_key': request.session.session_key, 'message': 'not authenticated'})

@login_required
def req_login(request):
    username = request.user.username
    return JsonResponse({"username": username})