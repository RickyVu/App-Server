from django.middleware import csrf
from django.http import HttpResponse, JsonResponse

def initiate(request):
    session_id = request.session.session_key
    return JsonResponse({"session_id": session_id})