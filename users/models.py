from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(username, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    description = models.TextField(max_length=500, blank=True)
    profile_picture_path = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='myuser_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='myuser_permissions')

    objects = MyUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['password', 'username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'MyUser'
        verbose_name_plural = 'MyUsers'