from api.models import *
from api.serializers import *
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()