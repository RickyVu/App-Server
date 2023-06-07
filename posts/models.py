from django.db import models
from users.models import MyUser
from media.models import Image, Video
import uuid
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

class PostContent(models.Model):
    poster = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, default="")
    text_content = models.TextField(default="")
    pub_date = models.DateTimeField(auto_now_add = True)
    pub_location = models.CharField(max_length=100, null=True)
    images = models.ManyToManyField(Image, related_name="postcontents")
    videos = models.ManyToManyField(Video, related_name="postcontents")
    tags = models.ManyToManyField(Tag)
    like_users = models.ManyToManyField(MyUser, related_name="liked_posts")
    favourite_users = models.ManyToManyField(MyUser, related_name="favourited_posts")

    def __str__(self):
        return f"{self.id}:{self.title}"

    def get_images_url(self):
        return [image.get_url() for image in self.images.all()]

    def get_videos_url(self):
        return [video.get_url() for video in self.videos.all()]

    def get_tag_names(self):
        return [tag.tag_name for tag in self.tags.all()]

    def get_like_count(self):
        return len(self.like_users.all())

    def get_favourite_count(self):
        return len(self.favourite_users.all())



