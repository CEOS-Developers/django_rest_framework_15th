from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content', 'isMedia']


class ProfileSerializer(serializers.ModelSerializer):
    this_post = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'introduction', 'profileImg', 'this_post']


class CommentSerialize(serializers.ModelSerializer):
    Comment_writer = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['content']

    def get_comment_writer(self, obj):
        return obj.Comment.user


class MediaSerializer(serializers.ModelSerializer):
    Own_post = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ['url', 'type']

    def get_own_post(self, obj):
        return obj.Media.post


class LikeSerializer(serializers.ModelSerializer):
    own_post = serializers.SerializerMethodField()
    like_user = serializers.SerializerMethodField()

    class Meta:
        model = Like

    def get_own_post(self, obj):
        return obj.Like.post

    def get_like_user(self, obj):
        return obj.Like.user
