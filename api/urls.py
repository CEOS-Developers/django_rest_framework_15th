from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/profiles', views.ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

