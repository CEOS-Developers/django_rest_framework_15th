from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'create_date']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['user', 'content', 'create_date', 'comments']