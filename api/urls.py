from django.urls import path
from . import views


urlpatterns = [
    path('api/comments', views.comment_api),
    path('api/likes', views.like_api),
    path('api/medias', views.media_api),
    path('api/posts', views.post_api),
    path('api/profiles', views.profile_api)
]
