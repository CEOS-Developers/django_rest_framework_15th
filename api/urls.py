from django.urls import path
from api import views
from api.views import *

urlpatterns = [
    path('posts/', PostList.as_view()),
    path('posts/<int:pk>/', PostDetail.as_view())
]