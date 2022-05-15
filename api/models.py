from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

# 장고는 기본적으로 기본키 설정 (id = models.AutoField(primary_key=True))을 제공


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # 해당 레코드 생성 시 현재 시간 자동 저장
    updated_at = models.DateTimeField(auto_now=True)  # 해당 레코드 갱신 시 현재 시간 자동 저장
    status = models.CharField(max_length=20, default='valid')

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    nickname = models.CharField(max_length=30, unique=True)
    profile_scripts = models.TextField(blank=True)
    profile_image = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.nickname


class Following(BaseModel):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followerUser')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followingUser')

    def __str__(self):
        return '{} : {}'.format(self.follower.nickname, self.following.nickname)


class Location(BaseModel):
    name = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()

    def __str__(self):
        return self.name


class Post(BaseModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')
    script = models.TextField(blank=True)
    type = models.CharField(max_length=20)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, blank=True, related_name='related_location_post')
    liking_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} : {}'.format(self.author, self.type)


class Image(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')
    url = models.TextField()


class Movie(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='movie')
    url = models.TextField()


class Liking(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_like_posting')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')

    def __str__(self):
        return '{} : {}'.format(self.user.nickname, self.post.type)


class Comment(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_add_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    script = models.TextField()

    def __str__(self):
        return '{} : {} : {}'.format(self.user.nickname, self.post.type, self.script)


class Story(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_upload_story')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='story')

    def __str__(self):
        return '{} : {}'.format(self.user.nickname, self.id)


class ViewingStory(BaseModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='viewing_story')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='viewer')
    liking = models.IntegerField()

    def __str__(self):
        return '{} : {}'.format(self.user.nickname, self.story.id)
