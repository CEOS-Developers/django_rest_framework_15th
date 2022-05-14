from django.http import JsonResponse, Http404
from rest_framework import status, mixins
from rest_framework.views import APIView
from rest_framework import viewsets
from api.models import Profile, Post
from api.serializers import *
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend


# Viewset
# Profile
class ProfileViewset(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


# Filter
class PostFilter(FilterSet):
    """Filter for Posts by if posts are archived or not"""
    profile = filters.CharFilter(field_name='profile', method='filter_profile')
    archived = filters.BooleanFilter(field_name='archived_flag', method='filter_archived')

    class Meta:
        model = Post
        fields = ['profile', 'archived_flag']

    def filter_archived(self, queryset, name, value):
        lookup = '__'.join([name, 'isnull'])
        return queryset.filter(**{lookup: False})

    def filter_profile(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })


# Post
class PostViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    filterset_fields = ['profile', 'archived_flag']


# APIView
'''
# profile
class ProfileList(APIView):
    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


class ProfileDetail(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return JsonResponse({"code": "200"}, status=status.HTTP_204_NO_CONTENT, safe=False)


# post
class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)

    def patch(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return JsonResponse({"code": "200"}, status=status.HTTP_204_NO_CONTENT, safe=False)
'''
