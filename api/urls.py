from django.urls import path
from . import views


urlpatterns = [
    path('api/comments', views.CommentList.as_view()),
    path('api/comments/<int:pk>/', views.CommentDetail.as_view()),
    path('api/likes', views.LikeList.as_view()),
    path('api/likes/<int:pk>/', views.LikeList.as_view()),
    path('api/medias', views.MediaList.as_view()),
    path('api/medias/<int:pk>/', views.MediaDetail.as_view()),
    path('api/posts', views.PostList.as_view()),
    path('api/posts/<int:pk>/', views.PostDetail.as_view()),
    path('api/profiles', views.ProfileList.as_view()),
    path('api/profiles/<int:pk>/', views.ProfileDetail.as_view())
]
