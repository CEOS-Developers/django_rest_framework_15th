from rest_framework import serializers
from api.models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'name', 'photo', 'website', 'bio', 'public_flag', 'number_follower',
                  'number_following', 'number_posts']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['profile', 'caption', 'location', 'count_like', 'count_comment', 'archived_flag', 'hide_count_flag',
                  'turnoff_comment_flag']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'profile', 'content', 'count_like']


class RecommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        fields = ['profile', 'parent_comment', 'content', 'count_like']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['post', 'file', 'order']


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post', 'profile']


class CommentLkeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLke
        fields = ['comment', 'profile']
