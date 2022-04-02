from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=20)
	site = models.TextField(null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	profile_img = models.ImageField(null=True, blank=True)

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True) # 생성
	like_count = models.PositiveIntegerField()
	comment_count = models.PositiveIntegerField()

class File(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	file = models.FileField()

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True) # 생성
	updated_at = models.DateTimeField(auto_now=True) # 수정

class Like(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
