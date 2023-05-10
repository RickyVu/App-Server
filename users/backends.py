from django.contrib.auth.backends import BaseBackend
from . import models

class MyAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = models.MyUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except models.MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return models.MyUser.objects.get(pk=user_id)
        except models.MyUser.DoesNotExist:
            return None