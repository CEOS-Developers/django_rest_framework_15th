from rest_framework import routers
from .views import FileViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'files', FileViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = router.urls
