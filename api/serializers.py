from rest_framework import serializers

from api.models import *
from django.contrib.auth.models import User


class FileSerializer(serializers.ModelSerializer):
    post_content = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'post_content', 'type', 'url']

    def get_post_content(self, obj):
        return obj.post.content


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']


class PostSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'like_count', 'files']
