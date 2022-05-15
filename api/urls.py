from django.urls import path
from api import views
from rest_framework import routers
from .views import *

# Viewset

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewset)
router.register(r'posts', PostViewset)

urlpatterns = router.urls

# APIView
'''
urlpatterns = [
    path('api/profiles', views.ProfileList.as_view()),
    path('api/profiles/<int:pk>', views.ProfileDetail.as_view()),
    path('api/posts', views.PostList.as_view()),
    path('api/posts/<int:pk>', views.PostDetail.as_view())
]
'''

