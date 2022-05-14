from api.models import *
from api.serializers import *
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend


class PostFilter(FilterSet):
	user = filters.NumberFilter(field_name='user')

	class Meta:
		model = Post
		fields = '__all__'

class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()
	filter_backends = [DjangoFilterBackend]
	filterset_class = PostFilter