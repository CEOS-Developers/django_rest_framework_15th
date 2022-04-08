from django.contrib import admin
from api.models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Liking)
admin.site.register(Comment)
admin.site.register(Story)
admin.site.register(ViewingStory)
