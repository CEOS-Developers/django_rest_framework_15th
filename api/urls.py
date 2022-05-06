from django.urls import path
from api import views


urlpatterns = [
	# post
	path('posts/', views.PostList.as_view()),
	path('posts/<int:pk>/', views.PostDetail.as_view()),
	# profile
	path('profiles/', views.ProfileList.as_view()),
	path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
	# comment
	path('comments/', views.CommentList.as_view()),
	path('comments/<int:pk>/', views.CommentDetail.as_view()),
]
