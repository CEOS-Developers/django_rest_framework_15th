from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from api.serializers import *


class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
