from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from media.models import Image
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid

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
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False, null= False)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    description = models.TextField(max_length=500, blank=True)
    profile_picture = models.ForeignKey("media.Image", on_delete=models.SET_NULL, null=True)

    follow = models.ManyToManyField('self', related_name='user_follows', symmetrical=False)
    blacklist = models.ManyToManyField('self', related_name='user_blacklists', symmetrical=False)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='myuser_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='myuser_permissions')

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'MyUser'
        verbose_name_plural = 'MyUsers'

    def save(self, *args, **kwargs):
        if not self.pk:
            self._original_is_active = False
        else:
            orig = MyUser.objects.get(pk=self.pk)
            self._original_is_active = orig.is_active
        super(MyUser, self).save(*args, **kwargs)

@receiver(post_save, sender=MyUser)
def create_user_image(sender, instance, created, **kwargs):
    if created:
        profile_picture_model = Image()
        profile_picture_model.name = profile_picture_model.generate_file_name()
        profile_picture_model.save()
        instance.profile_picture = profile_picture_model

        instance.save()
