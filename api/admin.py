from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('profile', 'caption', 'count_like', 'count_comment')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'number_follower', 'number_following')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)


admin.site.register(Comment)
admin.site.register(Recomment)
admin.site.register(File)
admin.site.register(Tag)
admin.site.register(Alttext)
admin.site.register(Hashtag)
admin.site.register(PostLike)
admin.site.register(CommentLke)


