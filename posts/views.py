from django.shortcuts import render
from PIL import Image as Img
from media.models import Image, Video
from . import models
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
import json
import m3u8
import os
import io
import shutil
import ffmpeg_streaming
import traceback


def mpd(request):
    #hls = m3u8.load("/home/RickyVu/App-Server/assets/videos/output.m3u8")
    #return HttpResponse(hls)
    """
    m3u8_path = '/home/RickyVu/App-Server/assets/videos/output.m3u8'
    file_size = os.path.getsize(m3u8_path)
    with open(m3u8_path, 'rb') as f:
        response = StreamingHttpResponse(f, content_type='application/vnd.apple.mpegurl')
        #response['Content-Length'] = file_size
        return response"""

    """from ffmpeg_streaming import Formats

    path = '/home/RickyVu/App-Server/assets/videos/test1.mp4'
    video = ffmpeg_streaming.input(path)


    dash = video.dash(Formats.h264())
    dash.auto_generate_representations()
    dash.output()
    return HttpResponse("transcoded")"""
    mpd_path = '/home/RickyVu/App-Server/assets/videos/test1.mpd'
    with open(mpd_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/dash+xml')
        response['Content-Length'] = os.path.getsize(mpd_path)
        return response

def segment(request, segment_name):
    segment_path = '/home/RickyVu/App-Server/assets/videos/' + segment_name
    with open(segment_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(segment_path)
        return response

@login_required
def test(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        image_data = request.FILES.get('image')
        video_data = request.FILES.get('video')


        # Do something with the uploaded files
        if title:
            pass
        if text:
            # Handle the text file
            pass
        if image_data:
            # Handle the image file
            # Initiate an Image model
            # Need to save first, then auto increment value will be generated
            image_model = Image()
            image_model.upload_user = request.user
            image_model.save()

            #image_path = settings.STATIC_URL+"images/"+image_model.get_file_name()
            image_path = os.path.join(settings.BASE_DIR, "assets", "images", image_model.get_file_name())


            # Open the image data as an image object
            image = Img.open(image_data)

            """# Save the image in JPEG format with a quality of 90
            buffer = BytesIO()
            image.save(buffer, 'JPEG', quality=90)

            # Get the buffered value and write it to a file
            image_file = open(image_path, 'wb')
            image_file.write(buffer.getvalue())
            image_file.close()"""


            # Save the image to a file
            image.save(image_path, 'JPEG', quality=70)

        if video_data:
            video_path = os.path.join(settings.BASE_DIR, "assets", "videos", video_data.name)
            # Save the uploaded file to disk
            default_storage.save(video_path, video_data)


        # Return a response
        return JsonResponse({'success': True, 'message': 'upload successful'})

    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)



@csrf_exempt
def retrieve(request):
    """
    request:
    {
        "start": ""|string (post_id)
        "count": int,
        "filter_by": ""|"username"|"text"|"location"|"tags"
        "key_words": list<string>,
        "order_by": ""|"date"|"likes"|"favourites"
        "order": "asc"|"desc"
    }

    """
    if request.method=="POST":
        try:
            #for t in models.PostContent.objects.all():
            #    t.delete()
            data = json.loads(request.body)
            #data = request.POST
            start = data["start"]
            count = data["count"]
            filter_by = data["filter_by"]
            key_words = data["key_words"]
            order_by = data["order_by"]
            order = data["order"]

            allowed_filters = ("username", "text", "location", "tags")
            allowed_orders = ("date", "likes", "favourites")

            filtered = models.PostContent.objects.none()
            if filter_by in allowed_filters:

                for key_word in key_words:
                    if filter_by=="username":
                        filtered|= models.PostContent.objects.filter(poster__username=key_word)
                    elif filter_by=="text":
                        filtered|= models.PostContent.objects.filter(title__icontains=key_word) | models.PostContent.objects.filter(text_content__icontains=key_word)
                    elif filter_by=="location":
                        filtered|= models.PostContent.objects.filter(post_location__icontains=key_word)
                    elif filter_by=="tags":
                        filtered |= models.PostContent.objects.filter(tags__tag_name=key_word)
            else:
                filtered = models.PostContent.objects.all()

            ordered = filtered
            if order_by not in allowed_orders:
                order_by = "date"
            orderByMap = {"date":"pub_date", "likes": "like_users", "favourites": "favourite_users"}
            if order_by=="date":
                order_field = orderByMap[order_by]
            elif order_by=="likes":
                order_field = "num_likes"
                ordered = ordered.annotate(num_likes=Count(orderByMap[order_by])).first()
            elif order_by=="favourites":
                order_field = "num_favourites"
                ordered = ordered.annotate(num_favourites=Count(orderByMap[order_by])).first()


            if order!="asc":
                order_field = "-"+order_field
            ordered = ordered.order_by(order_field)
            #ordered = ordered.order_by("pub_date")

            #filtered = models.PostContent.objects.filter(title__icontains=key_word)
            #filtered = models.PostContent.objects.filter(text_content__icontains=key_word)
            #filtered = MyModel.objects.filter(Q(title__icontains=key_word) | Q(text_content__icontains=key_word))
            #orderedmodels.PostContent.objects.filterorder_by(order_by)[:count]

            if start!="":
                start_post = models.PostContent.objects.get(id=start)
                sliced = list(ordered)
                start_index = sliced.index(start_post)+1
                sliced = sliced[start_index: start_index+count]
            else:
                sliced = list(ordered)[:count]

            json_result = [{"user": post.poster.username,
                            "user_id": post.poster.id,
                            "title": post.title,
                            "id": post.id,
                            "text": post.text_content,
                            "images": post.get_images_url(),
                            "videos": post.get_videos_url(),
                            "tags": post.get_tag_names(),
                            "pub_date": post.pub_date,
                            "pub_location": post.pub_location,
                            "likes": post.get_like_count(),
                            "favourites": post.get_favourite_count()} for post in sliced]

            return JsonResponse({'success': True, "message": json_result, "test": [order_field]})

        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success': False, 'message': 'invalid request, need to query parameters: start, count, filter_by, key_words, order_by, order'+traceback.format_exc()}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@login_required
def post(request):
    """
    poster = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="")
    text_content = models.TextField(default="")
    pub_date = models.DateField(auto_now = True)
    pub_location = models.CharField(max_length=100, null=True)
    images = models.ManyToManyField(Image, null=True)
    videos = models.ManyToManyField(Video, null=True)
    tags = models.ManyToManyField(Tag, null=True)
    """

    IMAGE_COUNT = 9
    VIDEO_COUNT = 1

    if request.method == 'POST':
        try:
            post = models.PostContent(poster = request.user)

            title = request.POST.get('title')
            post.title = title

            text_content = request.POST.get('text_content')
            post.text_content = text_content

            post.save()


            for i in range(1, IMAGE_COUNT+1):
                image_data = request.FILES.get(f"image-{i}")

                if image_data:
                    # Initiate an Image model, save so that primary key will be auto generated
                    image_model = Image()
                    image_model.save()

                    image_path = image_model.get_full_path()

                    #image = Img.open(image_data)
                    #image.save(image_path, 'JPEG', quality=70)
                    default_storage.save(image_path, image_data)
                    post.images.add(image_model)
                    post.save()


            for i in range(1, VIDEO_COUNT+1):
                video_data = request.FILES.get(f"video-{i}")

                if video_data:
                    # Initiate an Image model, save so that primary key will be auto generated
                    video_model = Video()
                    video_model.save()

                    post.videos.add(video_model)
                    post.save()

            post.save()

            # Return a response
            return JsonResponse({'success': True, 'message': 'upload successful'})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)


    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@login_required
def like(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            post_id = data['id']

            post = models.PostContent.objects.get(id=post_id)

            if request.user in post.like_users.all():
                post.like_users.remove(request.user)
            else:
                post.like_users.add(request.user)
            post.save()

            # Return a response
            return JsonResponse({'success': True, 'message': 'liked'})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)

@login_required
def favourite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            post_id = data['id']

            post = models.PostContent.objects.get(id=post_id)

            if request.user in post.favourite_users.all():
                post.favourite_users.remove(request.user)
            else:
                post.favourite_users.add(request.user)
            post.save()

            # Return a response
            return JsonResponse({'success': True, 'message': 'favourited'})
        except:
             return JsonResponse({'success': False, 'message': 'ERROR: '+traceback.format_exc()}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'method not allowed'}, status=405)
