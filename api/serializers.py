from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
	user_name = serializers.SerializerMethodField()

	class Meta:
		model = Comment
		fields = ['id', 'post', 'user', 'user_name', 'content', 'created_at', 'updated_at']

	def get_user_name(self, obj):
		return obj.user.name


class LikeSerializer(serializers.ModelSerializer):
	user_name = serializers.SerializerMethodField()

	class Meta:
		model = Like
		fields = ['id', 'post', 'user', 'user_name', 'created_at', 'updated_at']

	def get_user_name(self, obj):
		return obj.user.name


class FileSerializer(serializers.ModelSerializer):
	class Meta:
		model = File
		fields = ['id', 'post', 'type', 'path']


class PostSerializer(serializers.ModelSerializer):
	user_name = serializers.SerializerMethodField()
	files = FileSerializer(many=True, read_only=True)
	comments = CommentSerializer(many=True, read_only=True)
	likes = LikeSerializer(many=True, read_only=True)

	class Meta:
		model = Post
		fields = ['id', 'user', 'user_name', 'content', 'like_count', 'comment_count', 'created_at', 'updated_at', 'files', 'comments', 'likes']

	def get_user_name(self, obj):
		return obj.user.name


class ProfileSerializer(serializers.ModelSerializer):
	posts = PostSerializer(many=True, read_only=True)

	class Meta:
		model = Profile
		fields = ['id', 'user', 'name', 'site', 'bio', 'profile_img', 'posts']
