from api.serializers import *
from api.models import *
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend


class PostFilter(FilterSet):
    user = filters.CharFilter(method='filter_user')  # method

    def filter_user(self, queryset, name, value):
        filtered_queryset = queryset.filter(user=value)
        return filtered_queryset


class CommentFilter(FilterSet):
    post = filters.NumberFilter(field_name='post')

    class Meta:
        model = Comment
        fields = ['post']


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter