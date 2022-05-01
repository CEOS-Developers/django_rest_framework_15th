from django.urls import path
from api import views

urlpatterns = [
    path('api/profiles', views.profile_list),
    path('api/posts', views.post_list),
]
