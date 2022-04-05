from django.urls import path
from api import views

urlpatterns = [
    path('files/', views.file_list)
]