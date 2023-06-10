from . import models
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from media.models import Image
import traceback
import uuid
from users.checks import session_maintain, require_login

@session_maintain
def is_logged_in(request):
    if request.user.is_authenticated:
        return JsonResponse({'success': True, 'message': 'logged in'})
    return JsonResponse({'success': False, 'message': 'not logged in'})

@session_maintain
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
                user_id = user.id
                user.is_active = True
                user.save()
                return JsonResponse({'success': True, 'message': {"id": user_id}})
            else:
                # Handle invalid login credentials
                return JsonResponse({'success': False, 'message': 'invalid login credentials'})
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success': False, 'message': 'invalid request'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@session_maintain
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

@require_login
def log_out(request):
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    return JsonResponse({'message': 'logout successful'})

@session_maintain
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

@session_maintain
def description(request):
    if request.method == 'GET':
        user_id = request.GET.get('id')
        if user_id:
            user = models.MyUser.objects.get(id=int(user_id))
        else:
            user = request.user
        result = {'description':user.description}
        return JsonResponse({'success': True, 'message': result})
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@session_maintain
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

@session_maintain
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

@session_maintain
def username(request):
    if request.method == "GET":
        user_id = request.GET.get('id')
        if user_id:
            user = models.MyUser.objects.get(id=int(user_id))
        else:
            user = request.user
        #image_path = os.path.join(settings.BASE_DIR, "assets", "images", user.profile_picture.get_url())
        username = user.username
        return JsonResponse({'success': True, 'message': {"username": username}})
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@require_login
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

@require_login
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

@require_login
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

@require_login
def change_profile_picture(request):
    if request.method == "POST":
        try:
            user = request.user
            new_profile_picture_data = request.FILES.get("image")

            #image_model = Image.objects.create()
            #user.profile_picture = image_model
            #user.save()
            image_model = user.profile_picture
            image_path = image_model.get_full_path()
            default_storage.delete(image_path)

            image_model.name = image_model.generate_file_name()
            image_model.save()
            user.profile_picture = image_model
            user.save()

            new_path = image_model.get_full_path()
            #image = Img.open(new_profile_picture_data)

            #image.save(image_path, 'JPEG', quality=70)
            #default_storage.save(image_path, new_profile_picture_data)
            with open(new_path, 'wb+') as destination:
                for chunk in new_profile_picture_data.chunks():
                    destination.write(chunk)


            return JsonResponse({'success': True, 'message': 'change profile picture successful', "Image ID:": image_model.id, "path": image_path})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'success':False, 'message': 'invalid request'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)
"""
GET
users/blacklist?id=user_id
[{'user_id': user_id, 'username': username, 'profile_picture': url}]

POST
users/blacklist/
request: {'id': user_id} user_id of user going into blacklist


DELETE
users/blacklist/
request: {'id': user_id} user_id of user removing from blacklist

"""
@require_login
def blacklist(request):
    if request.method=="GET":
        try:
            user_id = request.GET.get("id")
            if not user_id:
                user = request.user
            else:
                user = models.MyUser.objects.get(id=user_id)

            blacklist_users = user.blacklist.all()

            result = [{'user_id': blacklist_user.id, 'username': blacklist_user.username, 'profile_picture': blacklist_user.profile_picture.get_url()} for blacklist_user in blacklist_users]

            # Return a response
            return JsonResponse({'success': True, 'message': result})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)
    if request.method=="POST":
        try:
            data = json.loads(request.body)

            blacklist_user_id = data['id']
            blacklist_user = models.MyUser.objects.get(id=blacklist_user_id)

            request.user.blacklist.add(blacklist_user)
            request.user.save()

            # Return a response
            return JsonResponse({'success': True, 'message': 'user added to blacklist'})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)
    elif request.method=="DELETE":
        try:
            data = json.loads(request.body)

            blacklist_user_id = data['id']
            blacklist_user = models.MyUser.objects.get(id=blacklist_user_id)

            request.user.blacklist.remove(blacklist_user)
            request.user.save()

            # Return a response
            return JsonResponse({'success': True, 'message': 'user removed from blacklist'})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@require_login
def follow(request):
    if request.method=="GET":
        try:
            user_id = request.GET.get("id")
            if not user_id:
                user = request.user
            else:
                user = models.MyUser.objects.get(id=user_id)

            follow_users = user.follow.all()

            result = [{'user_id': follow_user.id, 'username': follow_user.username, 'profile_picture': follow_user.profile_picture.get_url()} for follow_user in follow_users]

            # Return a response
            return JsonResponse({'success': True, 'message': result})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)
    if request.method=="POST":
        try:
            data = json.loads(request.body)

            follow_user_id = data['id']
            follow_user = models.MyUser.objects.get(id=follow_user_id)

            request.user.follow.add(follow_user)
            request.user.save()

            # Return a response
            return JsonResponse({'success': True, 'message': 'user added to follow'})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)
    elif request.method=="DELETE":
        try:
            data = json.loads(request.body)

            follow_user_id = data['id']
            follow_user = models.MyUser.objects.get(id=follow_user_id)

            request.user.follow.remove(follow_user)
            request.user.save()

            # Return a response
            return JsonResponse({'success': True, 'message': 'user removed from follow'})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@require_login
def follower(request):
    if request.method=="GET":
        try:
            user_id = request.GET.get("id")
            if not user_id:
                user = request.user
            else:
                user = models.MyUser.objects.get(id=user_id)

            other_users = models.MyUser.objects.exclude(id=user.id)
            followers = other_users.filter(follow__id=user.id)

            result = [{'user_id': follower.id, 'username': follower.username, 'profile_picture': follower.profile_picture.get_url()} for follower in followers]

            # Return a response
            return JsonResponse({'success': True, 'message': result})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)

# How many people follow this user
@require_login
def follower_count(request):
    if request.method=="GET":

        user_id = request.GET.get("id")
        if not user_id:
            user = request.user
        else:
            user = models.MyUser.objects.get(id=user_id)

        other_users = models.MyUser.objects.exclude(id=user.id)
        count = other_users.filter(follow__id=user.id).count()


        result = {"count": count}
        # Return a response
        return JsonResponse({'success': True, 'message': result})

        return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)

# How many people this user follows
@require_login
def follow_count(request):
    if request.method=="GET":

        user_id = request.GET.get("id")
        if not user_id:
            user = request.user
        else:
            user = models.MyUser.objects.get(id=user_id)

        result = {"count": user.follow.count()}
        # Return a response
        return JsonResponse({'success': True, 'message': result})

        return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)

@require_login
def is_following(request):
    if request.method=="GET":

        target_user_id = request.GET.get("id")
        if not target_user_id:
            return JsonResponse({'success': False, 'message': 'require supply id'})

        target_user = models.MyUser.objects.get(id=target_user_id)
        user = request.user
        result = {"yes":False}
        if target_user in user.follow.all():
            result["yes"] = True

        # Return a response
        return JsonResponse({'success': True, 'message': result})
    else:
        return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)

@require_login
def is_blacklisted(request):
    if request.method=="GET":

        target_user_id = request.GET.get("id")
        if not target_user_id:
            return JsonResponse({'success': False, 'message': 'require supply id'})

        target_user = models.MyUser.objects.get(id=target_user_id)
        user = request.user
        result = {"yes":False}
        if target_user in user.blacklist.all():
            result["yes"] = True

        # Return a response
        return JsonResponse({'success': True, 'message': result})
    else:
        return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)

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