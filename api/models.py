from django.db import models
from django.contrib.auth.models import User

class DateTime(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=20, unique=True)
	site = models.CharField(max_length=300, null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	profile_img = models.ImageField(null=True, blank=True)

class Post(DateTime):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	content = models.TextField()
	like_count = models.PositiveIntegerField(default=0)
	comment_count = models.PositiveIntegerField(default=0)

class File(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	type = models.PositiveIntegerField() # 0: photo, 1: video
	file = models.CharField(max_length=300)

class Comment(DateTime):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	content = models.TextField()

class Like(DateTime):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
