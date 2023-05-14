from django.middleware import csrf
from django.http import JsonResponse
from django.utils import timezone

def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    # Get the expiration date of the session
    expiry_date = request.session.get_expiry_date()

    # Convert the expiration date to the local timezone
    expiry_date_local = timezone.localtime(expiry_date)
    # expiry_date_local.strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse({"session_id": session_id, "session_expiry_date": expiry_date_local.strftime("%Y-%m-%d %H:%M:%S")})

def get_csrf_token(request):
    return JsonResponse({"csrf_token": csrf.get_token(request)})