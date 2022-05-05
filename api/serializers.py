from rest_framework import serializers
from api.models import *


class LikeSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Liking
        fields = ['user_nickname']

    def get_user_nickname(self, obj):
        return obj.user.nickname


class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user_nickname', 'script']

    def get_user_nickname(self, obj):
        return obj.user.nickname


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField(read_only=True)
    liked_post = LikeSerializer(many=True, read_only=True, allow_null=True, source='liking_set')
    comment_post = CommentSerializer(many=True, read_only=True, allow_null=True, source='comment_set')

    class Meta:
        model = Post
        fields = ['id', 'author_nickname', 'status', 'script', 'type', 'liking_count', 'author', 'location', 'liked_post', 'comment_post', 'created_at', 'updated_at']

    def get_author_nickname(self, obj):
        return obj.author.nickname


class ProfileSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=True, read_only=True, source='post_set')
    user_like_posting = LikeSerializer(many=True, read_only=True, source='liking_set')
    user_add_comment = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Profile
        fields = '__all__'
