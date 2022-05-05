from django.contrib import admin
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'name', 'site', 'bio', 'profile_img']
	list_display_links = ['name', 'bio']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'content', 'like_count', 'comment_count', 'created_at', 'updated_at']
	list_display_links = ['id', 'content']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
	list_display = ['post', 'type', 'path']
	list_display_links = ['path']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['id', 'content', 'post', 'user']
	list_display_links = ['id', 'content']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
	list_display = ['id', 'post', 'user']
	list_display_links = ['id']
