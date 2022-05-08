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
	profile_img = models.CharField(max_length=300, null=True, blank=True)

	def __str__(self):
		return self.name


class Post(DateTime):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
	content = models.TextField()
	like_count = models.PositiveIntegerField(default=0)
	comment_count = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.content


class File(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
	type = models.PositiveIntegerField() # 0: photo, 1: video
	path = models.CharField(max_length=300)


class Comment(DateTime):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	content = models.TextField()

	def __str__(self):
		return self.content


class Like(DateTime):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
