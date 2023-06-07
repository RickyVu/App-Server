from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from . import models
from users.models import MyUser
from django.db.models import Q
from pushy import PushyAPI
import json

# Create your views here.

def get_message_thread(user1, user2):
    try:
        message_thread = models.MessageThread.objects.get(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))
    except models.MessageThread.DoesNotExist:
        message_thread = None
    return message_thread

@login_required
def send(request):
    """
    request:
    receiver
    type
    message


    """
    if request.method == "POST":
        sender = request.user
        receiver = MyUser.objects.get(username=request.POST["receiver"])
        type = request.POST["type"]
        message = request.POST["message"]

        if receiver and type and message:
            message_thread = get_message_thread(sender, receiver)
            if message_thread is None:
                message_thread = models.MessageThread(user1=sender, user2=receiver)
            new_message = models.Message(sender=sender, type=type, message=message)
            message_thread.messages.add(new_message)


            # Payload data you want to send to devices
            data = {'id': new_message.id, 'message': message, 'type':type, 'sender': sender.username}

            device_tokens = models.DeviceToken.objects.filter(user=receiver)
            for token in device_tokens:
                # Send the push notification with Pushy
                PushyAPI.sendPushNotification(data, token)

            return JsonResponse({'success': True, 'message': 'message sent'})
        else:
            # Token is not present in the URL
            return JsonResponse({'success': False, 'message': 'require receiver, type, message in supplied json'})

    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@login_required
def retrieve(request):
    if request.method == 'GET':
        message_id = request.GET.get('id')


        if message_id:
            message = models.Message.objects.get(id=message_id)
            message_thread = models.MessageThead.objects.filter(messages__id=message_id).first()

            sender = 1
            if message.sender != message_thread.user1:
                sender = 2
            result = [
                {'user1': message_thread.user1.id, 'user2': message_thread.user2.id},
                {'id': message.id, 'sender': sender, 'time': message.time, 'type': message.type, 'message': message.message}
            ]
            return JsonResponse({'success': True, 'message': result})
        else:
            return JsonResponse({'success': False, 'message': 'id not supplies'})


    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)


@login_required
def delete(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        message_id = data['id']

        message = models.Message.objects.get(id=message_id)
        message.delete()
        return JsonResponse({'success': True, 'message': 'delete database message successful'})

    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)


@login_required
def device(request):
    if request.method == "POST":
        data = json.loads(request.body)
        device_token = data['token']

        if device_token:
            # Token is present in the URL
            models.DeviceToken(user=request.user, token=device_token)
            return JsonResponse({'success': True, 'message': 'device registered'})
        else:
            # Token is not present in the URL
            return JsonResponse({'success': False, 'message': 'did not supply token'})
    elif request.method=="DELETE":
        data = json.loads(request.body)
        device_token_string = data['token']

        device_token = models.DeviceToken.objects.get(token=device_token_string, user=request.user)
        if device_token:
            device_token.delete()
            return JsonResponse({'success':True, 'message': 'device token deleted'})
        else:
            #not found
            return JsonResponse({'success': False, 'message': 'token not found'})


    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)
