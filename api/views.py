from api.serializers import *
from rest_framework import viewsets, mixins, permissions
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


class AuthorPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method == 'POST':
			return request.data['user'] == int(request.headers['user'])
		else:
			return True

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS: # 조회 요청
			return True
		return request.data['user'] == int(request.headers['user'])


class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()
	permission_classes = [AuthorPermission]


class ProfilePermission(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.id == int(request.headers['user'])


class ProfileViewSet(viewsets.ModelViewSet):
	serializer_class = ProfileSerializer
	queryset = Profile.objects.all()
	permission_classes = [ProfilePermission]


class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()
	permission_classes = [AuthorPermission]
