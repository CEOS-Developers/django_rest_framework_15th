from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status_msg = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=200, null=True, default='') #프로필 사진 저장할 url

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=True) #사진만 올리는 경우 null 허용
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    create_date = models.DateField(auto_now_add=True)

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, default='') #사진 저장할 url
    create_date = models.DateField(auto_now_add=True)