from django.db import models
from django.contrib.auth.models import User


class DatetimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(unique=True, max_length=20, blank=True, default="")
    website = models.CharField(max_length=200, blank=True)
    bio = models.CharField(max_length=200, blank=True)


class Post(DatetimeModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    like_count = models.PositiveIntegerField(default=0)


class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    url = models.CharField(max_length=200)


class Like(DatetimeModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(DatetimeModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
