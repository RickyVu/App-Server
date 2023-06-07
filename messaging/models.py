from django.db import models
from users.models import MyUser
import uuid
# Create your models here.

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey("users.MyUser", on_delete=models.CASCADE)
    time = models.DateField(auto_now = True)
    type = models.TextField()
    message = models.TextField()

    def __str__(self):
        return f"MESSAGE:{self.sender}[{self.time}][{self.message[25]}]"

class MessageThread(models.Model):
    user1 = models.ForeignKey("users.MyUser", on_delete=models.CASCADE, related_name='%(class)s_user1')
    user2 = models.ForeignKey("users.MyUser", on_delete=models.CASCADE, related_name='%(class)s_user2')
    messages = models.ManyToManyField(Message)

    class Meta:
        unique_together = ('user1', 'user2')

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
    user = models.ForeignKey("users.MyUser", on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
