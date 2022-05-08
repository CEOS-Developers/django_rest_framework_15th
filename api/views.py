from api.serializers import *
from api.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.shortcuts import get_object_or_404


class PostList(APIView):
	def get(self, request, format=None):
		posts = Post.objects.all()
		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
	def get_object(self, pk):
		return get_object_or_404(Post, pk=pk)

	def get(self, request, pk, format=None):
		post = self.get_object(pk)
		serializer = PostSerializer(post)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		post = self.get_object(pk)
		serializer = PostSerializer(post, data=request.data) # put/patch
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		post = self.get_object(pk)
		post.delete()
		return Response(status=HTTP_204_NO_CONTENT)


class ProfileList(APIView):
	def post(self, request, format=None):
		serializer = ProfileSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProfileDetail(APIView):
	def get_object(self, pk):
		return get_object_or_404(Profile, pk=pk)

	def get(self, request, pk, format=None):
		profile = self.get_object(pk)
		serializer = ProfileSerializer(profile)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		profile = self.get_object(pk)
		serializer = ProfileSerializer(profile, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CommentList(APIView):
	def get(self, request, format=None):
		comments = Comment.objects.all()
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
	def get_object(self, pk):
		return get_object_or_404(Comment, pk=pk)

	def put(self, request, pk, format=None):
		comment = self.get_object(pk)
		serializer = CommentSerializer(comment, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		comment = self.get_object(pk)
		comment.delete()
		return Response(status=HTTP_204_NO_CONTENT)
