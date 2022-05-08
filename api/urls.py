from django.conf.urls import url
from django.urls import path, include
from api import views

urlpatterns = [
    path('api/posts/', views.PostView.as_view()),
    path('api/posts/<int:pk>', views.PostDetailView.as_view()),
    path('api/profiles', views.ProfileView.as_view()),
    path('api/profiles/<int:pk>', views.ProfileDetailView.as_view()),
    path('api/likes/<int:pk>', views.LikeView.as_view()),
    path('api/comments/<int:pk>', views.CommentView.as_view()),
]
