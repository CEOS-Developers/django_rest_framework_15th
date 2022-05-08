from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProfileList(APIView):
    """
    사용자(프로필) 조회 /api/profiles GET
    """
    def get(self, request, format=None):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True);
        return Response(serializer.data)
    """
    사용자(프로필) 생성 /api/profiles POST
    """
    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetail(APIView):
    """
    Profile 모델 개체 하나를 찾을 함수. 다른 함수들에 쓰일 예정
    """
    def get_one(self,pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404
    """
    특정 Profile 조회 ./api/profiles/{pk}/ GET
    """
    def get(self, request, pk):
        profile = self.get_one(pk);
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    """
    특정 profile 수정 -> put(완전대체), patch(수정), post(patch 불가 사항에 대해 -> 재생성 개념?)
    일단 put 사용 ./api/profiles/{pk}/ PUT
    """
    def put(self, request, pk):
        profile = self.get_one(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    Profile 하나 삭제. /api/profiles/{pk}/ DELETE
    """
    def delete(self, request, pk, format=None):
        profile = self.get_one(pk)
        profile.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostList(APIView):
  def get(self):
      return ;


class PostDetail(APIView):
    def get_one(self):
        return;


class LikeList(APIView):
    def get(self):
        return ;


class LikeDetail(APIView):
    def get_one(self):
        return ;


class CommentList(APIView):
    def get(self):
        return;


class CommentDetail(APIView):
    def get_one(self):
        return


class MediaList(APIView):
    def get(self):
        return


class MediaDetail(APIView):
    def get_one(self):
        return
