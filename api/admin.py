from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
    'id', 'content', 'user','create_date')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)