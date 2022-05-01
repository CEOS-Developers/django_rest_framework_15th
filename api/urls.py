from django.conf.urls import url
from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('api/post/', views.post_api),
    path('api/post/<int:pk>', views.post_detail),
    path('api/profile', views.profile_api),
    path('api/profile/<int:pk>', views.profile_detail),
]
