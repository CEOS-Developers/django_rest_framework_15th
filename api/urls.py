from django.urls import path
from api import views

urlpatterns = [
    path('api/profiles', views.ProfileList.as_view()),
    path('api/profiles/<int:pk>', views.ProfileDetail.as_view()),
    path('api/posts', views.PostList.as_view()),
]
