from rest_framework import serializers
from api.models import *


class FileSerializer(serializers.ModelSerializer):
    # post_content = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'type', 'url']

    def get_post_content(self, obj):
        return obj.post.content


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']


def validate_semicolon(value):
    if ";" in value:
        raise serializers.ValidationError(";은 내용에 포함할 수 없습니다.")
    return value


class PostSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'like_count', 'files', 'profile']


class ProfileSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
