from django.conf.urls import url
from django.urls import path, include
from api import views

urlpatterns = [
    path('api/posts/', views.PostView.as_view()),
    path('api/posts/<int:pk>', views.PostDetailView.as_view()),
    path('api/profiles', views.ProfileView.as_view()),
    path('api/profiles/<int:pk>', views.ProfileDetailView.as_view()),
]
