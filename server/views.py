from django.middleware import csrf
from django.http import HttpResponse, JsonResponse

def initiate(request):
    csrf_token = csrf.get_token(request)
    request.session['csrf_token'] = csrf_token
    return JsonResponse({'csrf_token':csrf_token})