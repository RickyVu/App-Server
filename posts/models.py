from django.db import models
from users.models import MyUser
from media.models import Image, Video
import uuid
import pytz
#4.发布者id，信息id
#5.信息id，信息标题，文字内容，发布时间，发布地点
#6.图片id，图片的path，信息id
#7.视频id，视频的path，信息id
#8.标签id，标签名称
#9.标签id，信息id
#10.信息id，点赞用户id
#11.信息id，收藏用户id


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag_name = models.TextField(null=False)

    def __str__(self):
        return f"TAG:{self.tag_name}"

"""
class CommentsTimeManager(models.Manager):
    def get_queryset(self):
        hong_kong_tz = pytz.timezone('Asia/Hong_Kong')
        return super().get_queryset().annotate(
            c_created_at=models.ExpressionWrapper(
                models.F('create_at')
                .astimezone(hong_kong_tz),
                output_field=models.DateTimeField(),
            ),
        )
"""
class Comments(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    text_content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    #objects = CommentsTimeManager()

"""
class PostContentTimeManager(models.Manager):
    def get_queryset(self):
        hong_kong_tz = pytz.timezone('Asia/Hong_Kong')
        return super().get_queryset().annotate(
            c_pub_date=models.ExpressionWrapper(
                models.F('pub_date')
                .astimezone(hong_kong_tz),
                output_field=models.DateTimeField(),
            ),
        )
"""
class PostContent(models.Model):
    poster = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, default="")
    text_content = models.TextField(default="")
    text_type = models.CharField(max_length=100, default="string")
    pub_date = models.DateTimeField(auto_now_add = True)
    pub_location = models.CharField(max_length=100, null=True)
    images = models.ManyToManyField(Image, related_name="postcontents")
    videos = models.ManyToManyField(Video, related_name="postcontents")
    tags = models.ManyToManyField(Tag)
    like_users = models.ManyToManyField(MyUser, related_name="liked_posts")
    favourite_users = models.ManyToManyField(MyUser, related_name="favourited_posts")
    comments = models.ManyToManyField(Comments, related_name="post_comments")

    #objects = PostContentTimeManager()

    def __str__(self):
        return f"{self.id}:{self.title}"

    def get_images_url(self):
        return [image.get_url() for image in self.images.order_by("-upload_date").all()]

    def get_videos_url(self):
        return [video.get_url() for video in self.videos.all()]

    def get_tag_names(self):
        return [tag.tag_name for tag in self.tags.all()]

    def get_like_count(self):
        return len(self.like_users.all())

    def get_favourite_count(self):
        return len(self.favourite_users.all())



