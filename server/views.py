from django.middleware import csrf
from django.http import HttpResponse, JsonResponse

def initiate(request):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    return JsonResponse({"session_id": session_id})