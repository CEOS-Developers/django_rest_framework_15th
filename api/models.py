import datetime

from django.db import models
from django.utils import timezone


# 1
class Post(models.Model):                                           # 게시글
    id = models.AutoField(primary_key=True)                         # PK
    user = models.ForeignKey('User', on_delete=models.CASCADE)      # FK (user_id)
    caption = models.CharField(max_length=2200)                     # 내용
    location = models.CharField(max_length=100)                     # 위치
    count_like = models.IntegerField(default=0)                     # 좋아요 수
    count_comment = models.IntegerField(default=0)                  # 댓글 수
    created_at = models.DateTimeField(auto_now_add=True)            # 생성일
    updated_at = models.DateTimeField(null=True)                    # 수정일
    deleted_at = models.DateTimeField(null=True)                    # 삭제일
    is_archived = models.BooleanField(default=False)                # archive 여부
    is_hide_count = models.BooleanField(default=False)              # 좋아요 수 숨김 여부
    is_turnoff_comment = models.BooleanField(default=False)         # 댓글 기능 해제

    def __str__(self):
        return "{} {} {}".format(self.created_at, self.user.username, self.caption)
        # 출력 형식 = 생성일 + user_id + 내용


# 2
class Comment(models.Model):                                        # 댓글
    id = models.AutoField(primary_key=True)                         # PK
    post = models.ForeignKey('Post', on_delete=models.CASCADE)      # FK (post_id)
    user = models.ForeignKey('User', on_delete=models.CASCADE)      # FK (user_id)
    content = models.CharField(max_length=2200)                     # 내용
    count_like = models.IntegerField(default=0)                     # 좋아요 수
    comment = models.BigIntegerField(null=True)                     # (대댓글) 상위 댓글
    count_comment = models.IntegerField(default=0)                  # (대댓글) 하위 댓글 수
    created_at = models.DateTimeField(auto_now_add=True)            # 생성일
    updated_at = models.DateTimeField(null=True)                    # 수정일
    deleted_at = models.DateTimeField(null=True)                    # 삭제일

    def __str__(self):
        return "{} {} {} {}".format(self.created_at, self.user.username, self.post.id, self.content)
        # 출력 형식 = 생성일 + user_id + post_id + 내용


# 3
class File(models.Model):                                           # 파일 only for image not video
    id = models.AutoField(primary_key=True)                         # PK
    post = models.ForeignKey('Post', on_delete=models.CASCADE)      # FK (post_id)
    file = models.FileField(upload_to='files/')                     # file 의 저장 위치
    order = models.IntegerField()                                   # post 의 file 순서
#    filter = models.IntegerField(default=0)                        # 사진 filter
    created_at = models.DateTimeField(auto_now_add=True)            # 생성일
    updated_at = models.DateTimeField(null=True)                    # 수정일
    deleted_at = models.DateTimeField(null=True)                    # 삭제일

    def __str__(self):
        return "{} {} {}".format(self.created_at, self.post.id, self.id)
        # 출력 형식 = 생성일 + post_id + file_id


# 4
class Tag(models.Model):                                            # Tag in image file
    id = models.AutoField(primary_key=True)                         # PK
    file = models.ForeignKey('File', on_delete=models.CASCADE)      # FK (file_id)
    user = models.ForeignKey('User', on_delete=models.CASCADE)      # FK (user_id)
    width = models.DecimalField(decimal_places=1, max_digits=3)     # tag 의 x 좌표
    height = models.DecimalField(decimal_places=1, max_digits=3)    # tag 의 y 좌표

    def __str__(self):
        return "{} {}".format(self.file.id, self.user.username)
        # 출력 형식 = file_id + user_id


# 5
class Alttext(models.Model):                                        # 대치 텍스트
    id = models.AutoField(primary_key=True)                         # PK
    file = models.ForeignKey('File', on_delete=models.CASCADE)      # FK (file_id)
    alt_text = models.CharField(max_length=125)                     # 내용

    def __str__(self):
        return "{} {}".format(self.file.id, self.alt_text)
        # 출력 형식 = file_id + 내용


# 6
class Hashtag(models.Model):                                        # Hashtag
    id = models.AutoField(primary_key=True)                         # PK
    post = models.ForeignKey('Post', on_delete=models.CASCADE)      # FK (post_id)
    tag = models.CharField(max_length=140)                          # tag

    def __str__(self):
        return "{} {}".format(self.post.id, self.tag)
        # 출력 형식 = post_id + tag


# 7
class PostLike(models.Model):                                       # 게시글 좋아요
    id = models.AutoField(primary_key=True)                         # PK
    post = models.ForeignKey('Post', on_delete=models.CASCADE)      # FK (post_id)
    user = models.ForeignKey('User', on_delete=models.CASCADE)      # FK (user_id)
    created_at = models.DateTimeField(auto_now_add=True)            # 생성일
    deleted_at = models.DateTimeField(null=True)                    # 삭제일

    def __str__(self):
        return "{} {}".format(self.post.id, self.user.username)
        # 출력 형식 = post_id + user_id


# 8
class CommentLke(models.Model):                                         # 댓글 좋아요
    id = models.AutoField(primary_key=True)                             # PK
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)    # FK (comment_id)
    user = models.ForeignKey('User', on_delete=models.CASCADE)          # FK (user_id)
    created_at = models.DateTimeField(auto_now_add=True)                # 생성일
    deleted_at = models.DateTimeField(null=True)                        # 삭제일

    def __str__(self):
        return "{} {}".format(self.comment.id, self.user.username)
        # 출력 형식 = comment_id + user_id


# 9
class User(models.Model):                                               # 사용자 User
    id = models.AutoField(primary_key=True)                             # PK
    username = models.CharField(max_length=30)                          # user_id
    password = models.CharField(max_length=32)                          # Hash 값 저장
    name = models.CharField(max_length=30)                              # 이름
    contact = models.CharField(max_length=320)                          # 내용
    birth = models.DateField()                                          # 생일
    profile = models.FileField(upload_to='file/profile/', null=True)    # 프로필 사진 저장 위치
    is_facebook_user = models.BooleanField(default=False)               # facebook 연동 계정
    is_verified_badge = models.BooleanField(default=False)              # verified_badge 계정
    number_follower = models.IntegerField(default=0)                    # 팔로워 수
    number_following = models.IntegerField(default=0)                   # 팔로잉 수
    is_public = models.BooleanField(default=False)                      # 공개 계정
    created_at = models.DateTimeField(auto_now_add=True)                # 생성일
    updated_at = models.DateTimeField(null=True)                        # 수정일
    deleted_at = models.DateTimeField(null=True)                        # 삭제일

    def __str__(self):
        return "{} {}".format(self.id, self.username)
        # 출력 형식 = id + user_id

# 10
# 모델 수정 필요
# class Follow(models.Model):                                       # Follow
#     id = models.AutoField(primary_key=True)                       # PK
#     user1 = models.ManyToManyField('User')                        # from user1
#     user2 = models.ManyToManyField('User')                        # to user2
#     created_at = models.DateTimeField(auto_now_add=True)          # 생성일
#     deleted_at = models.DateTimeField()                           # 삭제일
