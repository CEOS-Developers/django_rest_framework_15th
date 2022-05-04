
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,blank=True, null=True, on_delete=models.CASCADE)
    nickname = models.TextField(null=False, max_length=10)
    introduction = models.TextField(default='', max_length=200)
    profileImg = models.CharField(null=True, max_length=200)


class Post(models.Model):
    Profile = models.ForeignKey(Profile, default=-987654321, related_name='this_post', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    isMedia = models.BooleanField(default=True)


class Comment(models.Model):
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='ownPost', on_delete=models.CASCADE)
    content = models.TextField(blank=True)


class Media(models.Model):
    post = models.ForeignKey(Post, related_name='ownMedia',on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    type = models.CharField(max_length=20)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)







