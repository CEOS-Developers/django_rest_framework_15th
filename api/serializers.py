from rest_framework import serializers
from api.models import *


class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = ['id', 'follower', 'following', 'following_info']


class LikingSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Liking
        fields = ['post', 'user', 'user_nickname', 'created_at']

    def get_user_nickname(self, obj):
        return obj.user.nickname

    def get_created_at(self, obj):
        return Liking.objects.get(pk=obj.id).created_at.strftime("%Y-%m-%d %H:%M:%S")


class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['post', 'user', 'user_nickname', 'script', 'updated_at']

    def get_user_nickname(self, obj):
        return obj.user.nickname

    def get_updated_at(self, obj):
        return Comment.objects.get(pk=obj.id).updated_at.strftime("%Y-%m-%d %H:%M:%S")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField(read_only=True)
    post_liking = serializers.SerializerMethodField()
    post_comment = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_nickname', 'status', 'script', 'type', 'author', 'location',
                  'created_at', 'updated_at', 'liking_count', 'post_liking', 'post_comment']

    def get_author_nickname(self, obj):
        return obj.author.nickname

    def get_post_liking(self, obj):
        return list(Liking.objects.filter(post_id=obj.id).prefetch_related('post').values())

    def get_post_comment(self, obj):
        return list(Comment.objects.filter(post_id=obj.id).prefetch_related('post').values())

    def get_created_at(self, obj):
        return Post.objects.get(pk=obj.id).created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, obj):
        return Post.objects.get(pk=obj.id).updated_at.strftime("%Y-%m-%d %H:%M:%S")

    # @classmethod
    # def add_liking_count(cls):


class ProfileSerializer(serializers.ModelSerializer):
    user_post = serializers.SerializerMethodField()
    user_like_posting = serializers.SerializerMethodField()
    user_add_comment = serializers.SerializerMethodField()
    user_follower = serializers.SerializerMethodField()
    user_following = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'name', 'nickname', 'user_post', 'user_like_posting',
                  'user_add_comment', 'user_follower', 'user_following', 'created_at', 'updated_at', 'status']

    def get_user_post(self, obj):
        return list(Post.objects.filter(author_id=obj.id).prefetch_related('profile').values())

    def get_user_like_posting(self, obj):
        return list(Liking.objects.filter(user_id=obj.id).prefetch_related('profile').values())

    def get_user_add_comment(self, obj):
        return list(Comment.objects.filter(user_id=obj.id).prefetch_related('profile').values())

    def get_user_follower(self, obj):
        return list(Following.objects.filter(following_id=obj.id).prefetch_related('profile').values())

    def get_user_following(self, obj):
        return list(Following.objects.filter(follower_id=obj.id).prefetch_related('profile').values())

    def get_created_at(self, obj):
        return Profile.objects.get(pk=obj.id).created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, obj):
        return Profile.objects.get(pk=obj.id).updated_at.strftime("%Y-%m-%d %H:%M:%S")



