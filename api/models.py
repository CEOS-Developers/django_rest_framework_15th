import datetime

from django.db import models
from django.utils import timezone


# 1
class Post(models.Model):
    id = models.AutoField(primary_key=True)     # PK
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)     # FK
    caption = models.CharField(max_length=2200)
    location = models.CharField(max_length=100)
    count_like = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    is_archived = models.BooleanField(default=False)
    is_hide_count = models.BooleanField(default=False)
    is_turnoff_comment = models.BooleanField(default=False)


# 2
class Comment(models.Model):
    id = models.AutoField(primary_key=True)     # Automatic primary key
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)     # FK
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)     # FK
    content = models.CharField(max_length=2200)
    count_like = models.IntegerField(default=0)
    comment_id = models.BigIntegerField()   # comment of comment
    count_comment = models.IntegerField(default=0)  # comment number of comment
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


# 3 only for image not video
class File(models.Model):
    id = models.AutoField(primary_key=True)     # Automatic primary key
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)     # FK
    file = models.FileField(upload_to='files/')
    order = models.IntegerField()
    filter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


# 4
class Tag(models.Model):
    id = models.AutoField(primary_key=True)  # Automatic primary key
    file_id = models.ForeignKey('File', on_delete=models.CASCADE)     # FK
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)     # FK
    width = models.DecimalField(decimal_places=1, max_digits=3)
    height = models.DecimalField(decimal_places=1, max_digits=3)


# 5
class Alttext(models.Model):
    id = models.AutoField(primary_key=True)  # Automatic primary key
    file_id = models.ForeignKey('File', on_delete=models.CASCADE)     # FK
    alt_text = models.CharField(max_length=125)


# 6
class Hashtag(models.Model):
    id = models.AutoField(primary_key=True)  # Automatic primary key
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)     # FK
    hashtag = models.CharField(max_length=140)


# 7
class PostLike(models.Model):
    id = models.AutoField(primary_key=True)  # Automatic primary key
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)     # FK
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)     # FK
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)


# 8
class CommentLke(models.Model):
    id = models.AutoField(primary_key=True)  # Automatic primary key
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)     # FK
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)     # FK
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)


# 9
class User(models.Model):
    id = models.AutoField(primary_key=True)  # Automatic primary key
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=32)   # Hash
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=320)  # MAX LENGTH
    birth = models.DateField()
    is_facebook_user = models.BooleanField(default=False)
    is_verified_badge = models.BooleanField(default=False)
    number_follower = models.IntegerField(default=0)
    number_following = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)


# 10
# class Follow(models.Model):
#     id = models.AutoField(primary_key=True)  # Automatic primary key
#     user1 = models.ManyToManyField('User')
#     user2 = models.ManyToManyField('User')
#     created_at = models.DateTimeField(auto_now_add=True)
#     deleted_at = models.DateTimeField()
