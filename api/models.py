from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status_msg = models.CharField(max_length=100, null=True)

class Like(models.Model):
    like_cnt = models.IntegerField(null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=True) #사진만 올리는 경우 null 허용
    create_date = models.DateTimeField()

    def __str__(self):
        return self.content

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    create_date = models.DateTimeField()

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #photo = models.ImageField(upload_to="", blank=True, null=True)
    create_date = models.DateTimeField()