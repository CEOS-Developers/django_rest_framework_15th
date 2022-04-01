import datetime

from django.db import models
from django.utils import timezone


# 1
class Post(models.Model):
    id = models.BigIntegerField()       # key
    user_id # foreign key
    caption = models.CharField(max_length=2200)
    location = models.CharField(max_length=100)
    count_like = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    is_archived = models.BooleanField(default=False)
    is_hide_count = models.BooleanField(default=False)
    is_turnoff_comment = models.BooleanField(default=False)


# 2
class Comment(models.Model):
    id = models.BigIntegerField()           # key
    post_id  # foreign key
    user_id  # foreign key
    content = models.CharField(max_length=2200)
    count_like = models.IntegerField(default=0)
    comment_id = models.BigIntegerField()   # comment of comment
    count_comment = models.IntegerField(default=0)  # comment number of comment
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()


# 3 only for image not video
class File(models.Model):
    id = models.BigIntegerField()  # key
    post_id  # foreign key
    file = models.FileField(upload_to='files/')
    filter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()


# 4
class Tag(models.Model):
    id = models.BigIntegerField()   # key
    file_id  # foreign key
    user_id  # foreign key
    width = models.DecimalField(decimal_places=1, max_digits=3)
    height = models.DecimalField(decimal_places=1, max_digits=3)


# 5
class Alttext(models.Model):
    id = models.BigIntegerField()  # key
    file_id  # foreign key
    alt_text = models.CharField(max_length=125)



# 6
class Hashtag(models.Model):
    id = models.BigIntegerField()   # key
    post_id  # foreign key
    hashtag = models.CharField(max_length=140)


# 7
class PostLike(models.Model):
    id = models.BigIntegerField()   # key
    post_id # foreign key
    user_id # foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField()


# 8
class CommentLke(models.Model):
    id = models.BigIntegerField()   # key
    comment_id # foreign key
    user_id # foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField()


# 9
class User(models.Model):
    id = models.BigIntegerField()   # key
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
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()


# 10
class Follow(models.Model):
    id = models.BigIntegerField()   # key
    user1_id = models.BigIntegerField()
    user2_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField()
