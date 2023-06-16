from django.db import models
from users.models import MyUser
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from pushy import PushyAPI
# Create your models here.

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey("users.MyUser", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now = True)
    type = models.TextField()
    message = models.TextField()

    def __str__(self):
        return f"MESSAGE:{self.sender}[{self.time}][{self.message[25]}]"

'''
# Trigger when is_active of MyUser changes (when user logs in or out)
@receiver(post_save, sender=MyUser)
def on_is_active_change(sender, instance, **kwargs):
    if instance.is_active != instance._original_is_active:
        # if user is active
        # find related messages and send it via pushy
        if instance.is_active:

            query = Q(user1__exact=instance) | Q(user2__exact=instance)
            token_models = DeviceToken.objects.filter(user=instance)

            message_threads = MessageThread.exclude(messages__sender=instance).filter(query)
            for message in message_threads:
                data = {'id': str(message.id), 'message': message.message, 'type':message.type, 'sender': message.sender.username}
                for token_model in token_models:
                    PushyAPI.sendPushNotification(data, token_model.token)
                message.delete()
        else:
            pass
'''
class MessageThread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey("users.MyUser", on_delete=models.CASCADE, related_name='%(class)s_user1')
    user2 = models.ForeignKey("users.MyUser", on_delete=models.CASCADE, related_name='%(class)s_user2')
    messages = models.ManyToManyField(Message)

    class Meta:
        unique_together = ('user1', 'user2')

    def get_message_thread(user1, user2):
        try:
            message_thread = MessageThread.objects.get(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))
        except MessageThread.DoesNotExist:
            message_thread = MessageThread(user1=user1, user2=user2)
            message_thread.save()
        return message_thread

    def get_related_thread(user):
        query = Q(user1__exact=user) | Q(user2__exact=user)

        # Find records that match the query
        records = MessageThread.objects.filter(query)
        return records

    """

    thread
    [{},{},{}, ... {}]

    [
        {
            user1: $username
            user2: $username
        },

        {
            time: $time
            sender: 1|2
            type: 'string'|'image'|'video'
            message: $message
        }
    ]

    """

    def __str__(self):
        return f"CHAT:{self.user1}-{self.user2}"

class DeviceToken(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.MyUser", on_delete=models.CASCADE, related_name='device_tokens')
    is_active = models.BooleanField(default=False)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

'''
# Trigger when is_active of MyUser changes (when user logs in or out)
@receiver(post_save, sender=MyUser)
def on_is_active_change(sender, instance, **kwargs):
    if instance.is_active != instance._original_is_active:
        # if user is active
        # find related messages and send it via pushy
        if instance.is_active:

            query = Q(user1__exact=instance) | Q(user2__exact=instance)
            token_models = DeviceToken.objects.filter(user=instance)

            message_threads = MessageThread.exclude(messages__sender=instance).filter(query)
            for message in message_threads:
                data = {'id': str(message.id), 'message': message.message, 'type':message.type, 'sender': message.sender.username}
                for token_model in token_models:
                    PushyAPI.sendPushNotification(data, token_model.token)
                message.delete()
        else:
            pass
'''