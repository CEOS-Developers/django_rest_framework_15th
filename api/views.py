from api.serializers import *
from rest_framework import viewsets, mixins
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend


class PostFilter(FilterSet):
    user = filters.CharFilter(method='filter_user')
    content = filter.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['user', 'content']

    def filter_user(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })

class PostViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
