from django.db import models
from django.contrib.auth.models import User


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)            # 생성일
    updated_at = models.DateTimeField(auto_now=True)                # 수정일
    deleted_at = models.DateTimeField(null=True)                    # 삭제일

    class Meta:
        abstract = True


class Profile(CommonInfo):                                              # 프로필
    user = models.OneToOneField(User, on_delete=models.CASCADE)         # FK (user_id)
    name = models.CharField(max_length=30)                              # 이름
    photo = models.FileField(upload_to='file/profile/', null=True)      # 프로필 사진 저장 위치
    website = models.CharField(max_length=320)                          # Website
    bio = models.CharField(max_length=150)                              # Bio
    public_flag = models.BooleanField(default=False)                    # 공개 계정
    number_follower = models.IntegerField(default=0)                    # 팔로워 수
    number_following = models.IntegerField(default=0)                   # 팔로잉 수
    number_posts = models.IntegerField(default=0)                       # 게시글 수

    class Meta:
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Post(CommonInfo):                                                 # 게시글
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)    # FK (user_id)
    caption = models.CharField(max_length=2200)                         # 내용
    location = models.CharField(max_length=100)                         # 위치
    count_like = models.IntegerField(default=0)                         # 좋아요 수
    count_comment = models.IntegerField(default=0)                      # 댓글 수
    archived_flag = models.BooleanField(default=False)                  # archive 여부
    hide_count_flag = models.BooleanField(default=False)                # 좋아요 수 숨김 여부
    turnoff_comment_flag = models.BooleanField(default=False)           # 댓글 기능 해제

    def __str__(self):
        return "{} {} {}".format(self.created_at, self.profile.name, self.caption)
        # 출력 형식 = 생성일 + user_id + 내용

    class Meta:
        managed = True
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(CommonInfo):                                              # 댓글
    post = models.ForeignKey('Post', on_delete=models.CASCADE)          # FK (post_id)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)    # FK (user_id)
    content = models.CharField(max_length=2200)                         # 내용
    count_like = models.IntegerField(default=0)                         # 좋아요 수

    def __str__(self):
        return "{} {} {} {}".format(self.created_at, self.profile.name, self.post.id, self.content)
        # 출력 형식 = 생성일 + user_id + post_id + 내용

    class Meta:
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Recomment(CommonInfo):                                                    # 대댓글
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)            # FK (user_id)
    parent_comment = models.ForeignKey('Comment', on_delete=models.CASCADE)     # FK (comment_id) 상위 댓글
    content = models.CharField(max_length=2200)                                 # 내용
    count_like = models.IntegerField(default=0)                                 # 좋아요 수

    def __str__(self):
        return "{} {} {} {}".format(self.created_at, self.profile.name, self.parent_comment.id, self.content)
        # 출력 형식 = 생성일 + user_id + post_id + 내용

    class Meta:
        managed = True
        verbose_name = 'Recomment'
        verbose_name_plural = 'Recomments'


class File(CommonInfo):                                             # 파일 only for image not video
    post = models.ForeignKey('Post', on_delete=models.CASCADE)      # FK (post_id)
    file = models.FileField(upload_to='files/')                     # file 의 저장 위치
    order = models.IntegerField()                                   # post 의 file 순서
#    filter = models.IntegerField(default=0)                        # 사진 filter

    def __str__(self):
        return "{} {} {}".format(self.created_at, self.post.id, self.id)
        # 출력 형식 = 생성일 + post_id + file_id

    class Meta:
        managed = True
        verbose_name = 'File'
        verbose_name_plural = 'Files'


class Tag(models.Model):                                                # Tag in image file
    file = models.ForeignKey('File', on_delete=models.CASCADE)          # FK (file_id)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)    # FK (user_id)
    width = models.DecimalField(decimal_places=1, max_digits=3)         # tag 의 x 좌표
    height = models.DecimalField(decimal_places=1, max_digits=3)        # tag 의 y 좌표

    def __str__(self):
        return "{} {}".format(self.file.id, self.profile.name)
        # 출력 형식 = file_id + user_id

    class Meta:
        managed = True
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Alttext(models.Model):                                        # 대치 텍스트
    file = models.ForeignKey('File', on_delete=models.CASCADE)      # FK (file_id)
    alt_text = models.CharField(max_length=125)                     # 내용

    def __str__(self):
        return "{} {}".format(self.file.id, self.alt_text)
        # 출력 형식 = file_id + 내용

    class Meta:
        managed = True
        verbose_name = 'Alttext'
        verbose_name_plural = 'Alttexts'


class Hashtag(models.Model):                                        # Hashtag
    post = models.ForeignKey('Post', on_delete=models.CASCADE)      # FK (post_id)
    tag = models.CharField(max_length=140)                          # tag

    def __str__(self):
        return "{} {}".format(self.post.id, self.tag)
        # 출력 형식 = post_id + tag

    class Meta:
        managed = True
        verbose_name = 'Hashtag'
        verbose_name_plural = 'Hashtags'


class PostLike(models.Model):                                           # 게시글 좋아요
    post = models.ForeignKey('Post', on_delete=models.CASCADE)          # FK (post_id)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)    # FK (user_id)

    def __str__(self):
        return "{} {}".format(self.post.id, self.profile.name)
        # 출력 형식 = post_id + user_id

    class Meta:
        managed = True
        verbose_name = 'PostLike'
        verbose_name_plural = 'PostLikes'


class CommentLke(models.Model):                                         # 댓글 좋아요
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)    # FK (comment_id)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)    # FK (user_id)

    def __str__(self):
        return "{} {}".format(self.comment.id, self.profile.name)
        # 출력 형식 = comment_id + user_id

    class Meta:
        managed = True
        verbose_name = 'CommentLke'
        verbose_name_plural = 'CommentLkes'


# class User(models.Model):                                               # 사용자 User
#     username = models.CharField(max_length=30)                          # user_id
#     password = models.CharField(max_length=32)                          # Hash 값 저장
#     contact = models.CharField(max_length=320)                          # 연락처
#     birth = models.DateField()                                          # 생일
#     is_facebook_user = models.BooleanField(default=False)               # facebook 연동 계정
#     is_verified_badge = models.BooleanField(default=False)              # verified_badge 계정
#
#     def __str__(self):
#         return "{} {}".format(self.id, self.username)
#         # 출력 형식 = id + user_id

# 모델 수정 필요
# class Follow(models.Model):                                       # Follow
#     id = models.AutoField(primary_key=True)                       # PK
#     user1 = models.ManyToManyField('User')                        # from user1
#     user2 = models.ManyToManyField('User')                        # to user2
#     created_at = models.DateTimeField(auto_now_add=True)          # 생성일
#     deleted_at = models.DateTimeField()                           # 삭제일
