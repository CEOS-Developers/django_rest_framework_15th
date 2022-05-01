from django.contrib import admin
from .models import Post, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', "like_cnt", 'created_at', 'modified_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', "content", 'created_at', 'modified_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)