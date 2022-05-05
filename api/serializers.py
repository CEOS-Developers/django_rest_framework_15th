from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
	post_id = serializers.SerializerMethodField()
	user = serializers.SerializerMethodField()

	class Meta:
		model = Comment
		fields = ['post_id', 'user', 'content', 'created_at', 'updated_at']

	def get_post_id(self, obj):
		return obj.post.id

	def get_user(self, obj):
		return obj.user


class LikeSerializer(serializers.ModelSerializer):
	post_id = serializers.SerializerMethodField()
	user = serializers.SerializerMethodField()

	class Meta:
		model = Like
		fields = ['post_id', 'user', 'created_at', 'updated_at']

	def get_post_id(self, obj):
		return obj.post.id

	def get_user(self, obj):
		return obj.user


class FileSerializer(serializers.ModelSerializer):
	post_id = serializers.SerializerMethodField()

	class Meta:
		model = File
		fields = ['post_id', 'type', 'path']

	def get_post_id(self, obj):
		return obj.post.id


class PostSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	files = FileSerializer(many=True, read_only=True, source='file_set')
	comments = CommentSerializer(many=True, read_only=True, source='comment_set')
	likes = LikeSerializer(many=True, read_only=True, source='like_set')

	class Meta:
		model = Post
		fields = ['id', 'user', 'content', 'like_count', 'comment_count', 'created_at', 'updated_at', 'files', 'comments']

	def get_user(self, obj):
		return obj.user


class ProfileSerializer(serializers.ModelSerializer):
	posts = PostSerializer(many=True, read_only=True, source='post_set')

	class Meta:
		model = Profile
		fields = ['name', 'site', 'bio', 'profile_img', 'posts']
