from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from . import models
from users.models import MyUser
from users.checks import session_maintain, require_login
from pushy import PushyAPI
from django.db.models import Q
import json

# Create your views here.

'''
def get_message_thread(user1, user2):
    try:
        message_thread = models.MessageThread.objects.get(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))
    except models.MessageThread.DoesNotExist:
        message_thread = None
    return message_thread
'''
@require_login
def send(request):
    """
    request:
    receiver: id
    type: 'string'
    message: string


    """
    if request.method == "POST":
        data = json.loads(request.body)
        sender = request.user
        receiver = MyUser.objects.get(id=int(data["receiver"]))
        type = data["type"]
        message = data["message"]

        if receiver and type and message:
            '''
            message_thread = models.MessageThread.get_message_thread(sender, receiver)
            if message_thread is None:
                message_thread = models.MessageThread(user1=sender, user2=receiver)
            new_message = models.Message(sender=sender, type=type, message=message)
            message_thread.messages.add(new_message)
            '''

            new_message = models.Message(sender=sender, type=type, message=message)

            message_thread = models.MessageThread.get_message_thread(sender, receiver)

            # Payload data you want to send to devices
            data = {'id': str(new_message.id), 'message': message, 'type':type, 'sender': sender.username, "sender_id": sender.id}

            # Find all active devices of user
            active_device_token_models = models.DeviceToken.objects.filter(user=receiver, is_active=True)

            # if no active devices then we save it for later
            if active_device_token_models.count()==0:
                new_message.save()
                message_thread.messages.add(new_message)
                message_thread.save()
                return JsonResponse({'success': True, 'message': 'message stored'})


            # have active devices, send using pushy
            for active_device_token_model in active_device_token_models:
                messages = ""
                # Send the push notification with Pushy
                messages+="|"+PushyAPI.sendPushNotification(data, active_device_token_model.token)
            return JsonResponse({'success': True, 'message': 'message sent'+messages+str(models.DeviceToken.objects.all())})

            '''
            # Check if receiver is logged in
            if receiver.is_active:
                device_tokens = models.DeviceToken.objects.filter(user=receiver)
                messages = ""
                for token in device_tokens:
                    # Send the push notification with Pushy
                    messages+="|"+PushyAPI.sendPushNotification(data, token.token)
                return JsonResponse({'success': True, 'message': 'message sent'+messages+str(models.DeviceToken.objects.all())})
            else:
                #new_message = models.Message(sender=sender, type=type, message=message)
                new_message.save()
                message_thread.messages.add(new_message)
                message_thread.save()
                return JsonResponse({'success': True, 'message': 'message stored'+messages+str()})
            '''


        else:
            # Token is not present in the URL
            return JsonResponse({'success': False, 'message': 'require receiver, type, message in supplied json'})

    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@require_login
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


@require_login
def delete(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        message_id = data['id']

        message = models.Message.objects.get(id=message_id)
        message.delete()
        return JsonResponse({'success': True, 'message': 'delete database message successful'})

    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)


@require_login
def device(request):
    if request.method == "POST":
        #for t in models.DeviceToken.objects.all():
        #    t.delete()
        try:
            data = json.loads(request.body)
            device_token = data["token"]


            if device_token:
                # Token is present in the URL
                #token_model = models.DeviceToken.objects.get(user=request.user, token=device_token)
                #if not token_model:
                #    token_model = models.DeviceToken(user=request.user, token=device_token)

                token_model,created = models.DeviceToken.objects.get_or_create(user=request.user, token=device_token)
                if created:
                    token_model.save()
                token_model.is_active = True
                token_model.save()


                # Receive messages that are sent when user was logged out
                user = request.user

                query = Q(user1__exact=user) | Q(user2__exact=user)
                #message_threads = models.MessageThread.objects.filter(query)
                message_threads = models.MessageThread.objects.filter(query).exclude(messages__sender=user)
                for message_thread in message_threads:
                    for message in message_thread.messages.all():
                        data = {'id': str(message.id), 'message': message.message, 'type':message.type, 'sender': message.sender.username, "sender_id": message.sender.id}
                        PushyAPI.sendPushNotification(data, token_model.token)
                        message.delete()



                return JsonResponse({'success': True, 'message': 'device registered'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

        else:
            # Token is not present in the URL
            return JsonResponse({'success': False, 'message': 'did not supply token'})
    elif request.method=="DELETE":
        data = json.loads(request.body)
        device_token_string = data['token']

        device_token = models.DeviceToken.objects.get(token=device_token_string, user=request.user)
        if device_token:
            device_token.is_active = False
            device_token.save()
            #device_token.delete()
            return JsonResponse({'success':True, 'message': 'device token inactivated'})
        else:
            #not found
            return JsonResponse({'success': False, 'message': 'token not found'})


    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

def getall(request):
    if (len(list(models.DeviceToken.objects.all().values())))==0:
        return JsonResponse({"EMPTY": "NULL"})
    else:
        result = dict()
        for obj, values in zip(models.DeviceToken.objects.all(), models.DeviceToken.objects.all().values()):
            result[str(obj)] = values
        return JsonResponse(result)