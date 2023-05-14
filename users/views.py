from django.contrib.auth import authenticate, login, logout, get_user
from django.middleware import csrf
from django.http import HttpResponse, JsonResponse
from django.db.utils import IntegrityError
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
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
            return JsonResponse({'success': False, 'message': 'invalid request'})
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
                return JsonResponse({'success': False, "message": 'Fields cannot be empty'})
            try:
                user = models.MyUser.objects.create_user(username=username, password=password)
                user.save()
                return JsonResponse({'success': True, 'message': 'signup successful'})
            except IntegrityError:
                return JsonResponse({'success': False, "message": 'clashing unique fields'})

        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success': False, 'message': 'invalid request'})
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

def log_out(request):
    logout(request)
    print(request.session, request.session.session_key)
    return JsonResponse({'message': 'logout successful'})


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
    print(request.user, dir(request.user))
    username = request.user.username
    return JsonResponse({"username": username})