from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from api.models import *
from api.serializers import *
from rest_framework import exceptions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, get_list_or_404


class PostView(APIView):
    def get(self, request):
        post_list = Post.objects.all()
        serializer = PostSerializer(post_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class ProfileDetailView(APIView):
    def get(self, request, pk):
        try:
            get_profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(get_profile)
            return JsonResponse(serializer.data)
        except Profile.DoesNotExist:
            return JsonResponse(status=404)


class ProfileView(APIView):
    def get(self):
        profile_list = Profile.objects.all()
        serializer = ProfileSerializer(profile_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class PostDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, status=200)

    def put(self, request, pk):
        user_id = request.headers["userId"]
        data = JSONParser().parse(request)
        get_post = self.get_object(pk)
        serializer = PostSerializer(get_post, data=data)
        # Validation 처리 과정
        if serializer.is_valid():
            if get_post.author_id != int(user_id):
                raise exceptions.AuthenticationFailed()
            if get_post.author_id != data['author']:
                return Response(status=400)
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)

    def delete(self, request, pk):
        get_post = self.get_object(pk)
        user_id = request.headers["userId"]
        if get_post.author_id != int(user_id):
            raise exceptions.AuthenticationFailed()
        else:
            get_post.delete()
            return JsonResponse({"status": 201, "message": "SUCCESS"}, status=201, safe=False)
