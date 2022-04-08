from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post  # 사용할 모델
        fields = ['id', 'user', 'content', 'created_at', 'modified_at']  # 사용할 모델의 필드