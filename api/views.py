from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from api.serializers import *

from rest_framework.views import APIView



class PostDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    # 특정 Post 가져오기
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)

    # 특정 Post 업데이트하기
    def put(self, request, pk):
        data = JSONParser().parse(request)
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)

    # 특정 Post 삭제하기
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostList(APIView):
    # 모든 Post list 가져오기
    def get(self, request):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return JsonResponse(serializer.data, safe=False)

    # 새로운 Post 생성하기
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)

