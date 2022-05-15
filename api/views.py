from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from api.models import Profile, Post
from api.serializers import *
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend


# Profile
class ProfileFilter(FilterSet):
    user = filters.NumberFilter(field_name='user')  # profile 사용자
    name = filters.CharFilter(field_name='name', method='filter_name')  # profile name

    class Meta:
        model = Post
        fields = ['user', 'name']

    def filter_name(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })


class ProfileViewset(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfileFilter


# Post
class PostFilter(FilterSet):
    profile = filters.NumberFilter(field_name='profile')    # post 작성한 profile
    location = filters.CharFilter(field_name='location', method='filter_location')  # post location tag
    archived = filters.BooleanFilter(field_name='archived_flag')  # post 보관 유/무

    class Meta:
        model = Post
        fields = ['profile', 'location', 'archived_flag']

    def filter_location(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter




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
