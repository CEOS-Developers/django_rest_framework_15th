from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import *
from api.models import *
from rest_framework import status


class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        posts = self.get_object(pk)
        serializer = PostSerializer(posts)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        posts = self.get_object(pk)
        serializer = PostSerializer(posts, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        posts = self.get_object(pk)
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


