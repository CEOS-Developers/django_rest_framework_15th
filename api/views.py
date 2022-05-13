from api.serializers import *
from rest_framework import viewsets, mixins
from django_filters.rest_framework import FilterSet, filters, DjangoFilterBackend


class FileFilter(FilterSet):
	path = filters.CharFilter(field_name='path')
	type = filters.NumberFilter(method='filter_type')

	class Meta:
		model = File
		fields = ['path']

	def filter_type(self, queryset, name, value):
		filtered_queryset = queryset.filter(type=value)
		return filtered_queryset


class FileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	serializer_class = FileSerializer
	queryset = File.objects.all()
	filter_backends = [DjangoFilterBackend]
	filterset_class = FileFilter


class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
	serializer_class = ProfileSerializer
	queryset = Profile.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()
