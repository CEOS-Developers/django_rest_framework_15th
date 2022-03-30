from django.db import models
from django.contrib.auth.models import User

# 장고는 기본적으로 기본키 설정 (id = models.AutoField(primary_key=True))을 제공


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=30)
    profile_scripts = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 해당 레코드 생성 시 현재 시간 자동 저장
    updated_at = models.DateTimeField(auto_now=True)  # 해당 레코드 갱신 시 현재 시간 자동 저장
    status = models.CharField(max_length=20, default='valid')


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')


class Post(models.Model):
    POST_TYPE = (
        ("po", "Post"),
        ("re", "Reels")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    script = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=POST_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')


class Movie(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')


class Location(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')


class Liking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    script = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')


class ViewingStory(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liking = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default="valid")