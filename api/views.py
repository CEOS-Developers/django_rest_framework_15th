from rest_framework import viewsets, mixins
from api.serializers import *
from django_filters.rest_framework import FilterSet, filters, DjangoFilterBackend
from rest_framework import permissions


class FileFilter(FilterSet):
    url = filters.CharFilter(field_name='url', lookup_expr='icontains')
    type = filters.CharFilter(method='filter_by_type')

    class Meta:
        model = File
        fields = ['url']

    def filter_by_type(self, queryset, name, value):
        filtered_queryset = queryset.filter(type=value)
        return filtered_queryset


class FileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileFilter


class PostUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_authenticated


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [PostUpdatePermission,]
