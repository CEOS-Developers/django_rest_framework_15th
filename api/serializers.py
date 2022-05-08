from rest_framework import serializers
from .models import *

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['created_at']

class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post  # 사용할 모델
        fields = ['user', 'content', 'created_at', 'modified_at', 'likes']  # 사용할 모델의 필드