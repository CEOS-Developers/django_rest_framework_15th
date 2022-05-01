from rest_framework import serializers
from api.models import *


class LikeSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Liking
        fields = '__all__'

    def get_user_nickname(self, obj):
        return obj.user.nickname


class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_user_nickname(self, obj):
        return obj.user.nickname


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    liked_post = LikeSerializer(many=True, read_only=True, source='liking_set')
    comment_post = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Post
        fields = '__all__'

    def get_author_nickname(self, obj):
        return obj.author.nickname


class ProfileSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=True, read_only=True, source='post_set')
    user_like_posting = LikeSerializer(many=True, read_only=True, source='liking_set')
    user_add_comment = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Profile
        fields = '__all__'
