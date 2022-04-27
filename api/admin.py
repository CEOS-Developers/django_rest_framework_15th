from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'content', 'like_count', 'comment_count', 'created_at', 'updated_at']
	list_display_links = ['id', 'content']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
	list_display = ['post', 'type', 'path']
	list_display_links = ['path']


# Register your models here.
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Like)
