from django.db import models

#4.发布者id，信息id
#5.信息id，信息标题，文字内容，发布时间，发布地点
#6.图片id，图片的path，信息id
#7.视频id，视频的path，信息id
#8.标签id，标签名称
#9.标签id，信息id
#10.信息id，点赞用户id
#11.信息id，收藏用户id

class UserPost(models.Model):
    poster_id = models.CharField(max_length=32, null=False)
    post_id = models.CharField(max_length=30, primary_key=True, unique=True, null=False)
    

    def __str__(self):
        return f"{self.poster_id}'s {self.post_id}"

class PostContent(models.Model):
    post_id = models.ForeignKey(UserPost, on_delete=models.CASCADE, primary_key=True, unique=True, null=False)
    title = models.CharField(max_length=100, default="")
    text_content = models.TextField(default="")
    pub_date = models.DateField(auto_created=True, null=False)
    pub_location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.post_id}:{self.title}"
    
class PostImage(models.Model):
    post_id = models.ForeignKey(UserPost, on_delete=models.DO_NOTHING)
    image_id = models.CharField(max_length=30, primary_key=True)
    image_path = models.FileField()
    image_index = models.SmallIntegerField()




