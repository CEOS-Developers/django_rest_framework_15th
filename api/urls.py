from rest_framework import routers
from api.views import *


router = routers.DefaultRouter()
router.register(r'files', FileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
