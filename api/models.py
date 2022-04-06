from django.db import models
from django.contrib.auth.models import User

# 장고는 기본적으로 기본키 설정 (id = models.AutoField(primary_key=True))을 제공


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # 해당 레코드 생성 시 현재 시간 자동 저장
    updated_at = models.DateTimeField(auto_now=True)  # 해당 레코드 갱신 시 현재 시간 자동 저장
    status = models.CharField(max_length=20, default='valid')

    class Meta:
        abstract=True


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=30, unique=True)
    profile_scripts = models.TextField(blank=True, null=True)
    profile_image = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.nickname


class Following(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followingUser')

    def __str__(self):
        return self.user_id


class Follower(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followerUser')

    def __str__(self):
        return self.user_id


class Location(BaseModel):
    name = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()

    def __str__(self):
        return self.name


class Post(BaseModel):
    POST_TYPE = (
        ("po", "Post"),
        ("re", "Reels")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    script = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=POST_TYPE)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.type


class Image(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.TextField()


class Movie(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.TextField()


class Liking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    script = models.TextField()

    def __str__(self):
        return self.user_id


class Story(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class ViewingStory(BaseModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liking = models.IntegerField()

    def __str__(self):
        return self.story_id
