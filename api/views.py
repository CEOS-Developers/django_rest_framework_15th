from api.serializers import *
from rest_framework import viewsets, mixins


class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
	serializer_class = ProfileSerializer
	queryset = Profile.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()
