from django.urls import path
from django_rest_framework_15th.api import views


urlpatterns = [
    path('api/', views.comment_api),
    path('api/', views.like_api),
    path('api/', views.media_api),
    path('api/', views.post_api),
    path('api/', views.profile_api)
]
