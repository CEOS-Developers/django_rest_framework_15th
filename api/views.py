from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from api.serializers import *
from api.models import *


class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


