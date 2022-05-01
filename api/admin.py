from django.contrib import admin
from .models import *

# 출력할 PostAdmin 클래스
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'created_at', 'modified_at')

# 출력할 LikeAdmin 클래스
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at')

# 클래스를 Admin 사이트에 등록
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)