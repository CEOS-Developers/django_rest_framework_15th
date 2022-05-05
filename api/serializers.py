from rest_framework import serializers
from api.models import *


class LikingSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Liking
        fields = ['post', 'user', 'user_nickname', 'created_at']

    def get_user_nickname(self, obj):
        return obj.user.nickname



class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['post', 'user', 'user_nickname', 'script', 'created_at']

    def get_user_nickname(self, obj):
        return obj.user.nickname



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField(read_only=True)
    post_liking = serializers.SerializerMethodField()
    post_comment = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_nickname', 'status', 'script', 'type', 'author', 'location',
                  'created_at', 'updated_at', 'post_liking', 'post_comment']

    def get_author_nickname(self, obj):
        return obj.author.nickname

    def get_post_liking(self, obj):
        return list(Liking.objects.all().prefetch_related('post').values())

    def get_post_comment(self, obj):
        return list(Comment.objects.all().prefetch_related('post').values())

    # @classmethod
    # def add_liking_count(cls):



class ProfileSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=True, read_only=True, source='post_set')
    user_like_posting = LikingSerializer(many=True, read_only=True, source='liking_set')
    user_add_comment = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Profile
        fields = ['id', 'name', 'nickname', 'post', 'user_like_posting', 'user_add_comment', 'created_at', 'status']
