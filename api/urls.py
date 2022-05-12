from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'posts/', PostViewSet)
router.register(r'comments/', CommentViewSet)

urlpatterns = router.urls
