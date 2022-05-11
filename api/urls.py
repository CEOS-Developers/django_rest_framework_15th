from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .views import *
from api import views

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likings', LikingViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'followings', FollowingViewSet)
router.register(r'comments', CommentViewSet)
urlpatterns = router.urls

#
# urlpatterns = [
#     path('api/posts/', views.PostView.as_view()),
#     path('api/posts/<int:pk>', views.PostDetailView.as_view()),
#     path('api/profiles', views.ProfileView.as_view()),
#     path('api/profiles/<int:pk>', views.ProfileDetailView.as_view()),
#     path('api/likes/<int:pk>', views.LikeView.as_view()),
#     path('api/comments/<int:pk>', views.CommentView.as_view()),
# ]
