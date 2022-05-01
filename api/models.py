from django.db import models
from django.contrib.auth.models import User

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    profile_msg = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return self.name

class Post(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    like_cnt = models.IntegerField()

    def __str__(self):
        return self.content

class Comment(TimeStamp):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=225)

    def __str__(self):
        return self.content

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    path = models.TextField()
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name