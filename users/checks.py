from django.http import JsonResponse

def maintain_session(request):
    if request.session.get_expiry_age() <= 600:
        request.session.cycle_key()


def require_login(inner):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'require login'}, status=401)
        else:
            maintain_session(request)
            return inner(request, *args, **kwargs)
    return wrapper

def session_maintain(inner):
    def wrapper(request, *args, **kwargs):
        maintain_session(request)
        return inner(request, *args, **kwargs)
    return wrapper