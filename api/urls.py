from django.urls import path
from . import views


urlpatterns = [
    path('api/comment', views.comment_api),
    path('api/like', views.like_api),
    path('api/media', views.media_api),
    path('api/post', views.post_api),
    path('api/profile', views.profile_api)
]
