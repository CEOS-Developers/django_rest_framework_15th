from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
	post_id = serializers.SerializerMethodField()

	class Meta:
		model = File
		fields = '__all__'

	def get_post_id(self, obj):
		return obj.post.id


class PostSerializer(serializers.ModelSerializer):
	files = FileSerializer(many=True, read_only=True)

	class Meta:
		model = Post
		fields = ['id', 'user', 'content', 'like_count', 'comment_count', 'files']
