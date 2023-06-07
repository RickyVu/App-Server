from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model
from . import models
import uuid


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
"""
class UUIDBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            User = get_user_model()
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
"""
"""
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
            # Try to convert the user_id to a UUID
            uuid.UUID(user_id)
            return models.MyUser.objects.get(id=user_id)
        except (ValueError, TypeError, models.MyUser.DoesNotExist):
            # If the user_id is not a UUID or the user doesn't exist, return None
            return None
"""