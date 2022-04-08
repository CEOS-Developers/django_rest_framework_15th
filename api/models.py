from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True)
    profile_name = models.CharField(max_length=30, unique=True)
    profile_website = models.CharField(max_length=150, null=True, blank=True)
    profile_bio = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return 'userName : {}'.format(self.profile_name)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.content)

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.URLField(default='')
    type = models.CharField(max_length=10, default='')

    def __str__(self):
        return 'url : {}'.format(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} commented to {} post'.format(self.user, self.post)

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} replied to {} comment'.format(self.user, self.comment)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} liked {} post'.format(self.user, self.post)