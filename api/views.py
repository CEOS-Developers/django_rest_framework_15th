from django.http import JsonResponse

from api.serializers import *
from rest_framework import viewsets, exceptions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters
from api.permissions import *


class PostFilter(FilterSet):
    author = filters.NumberFilter(field_name='author')
    post_type = filters.CharFilter(method='type_filter')
    liking_count = filters.NumberFilter(field_name='liking_count')
    location = filters.NumberFilter(field_name='location_id')
    nickname = filters.CharFilter(field_name='author_id', lookup_expr="nickname__icontains")
    ordering = filters.OrderingFilter(
        fields=(
            ('author', 'userId'),
            ('created_at', 'date'),
            ('liking_count', 'like')
        )
    )

    def type_filter(self, queryset, name, value):
        filtered_queryset = queryset.filter(type=value)
        return filtered_queryset

    class Meta:
        model = Post
        fields = ['author', 'post_type', 'liking_count', 'location_id', 'nickname']


class LikingFilter(FilterSet):
    author = filters.CharFilter(field_name='user_id', lookup_expr='nickname__icontains')
    post_id = filters.NumberFilter(field_name='post_id')
    ordering = filters.OrderingFilter(
        fields=(
            ('created_at', 'date')
        )
    )

    class Meta:
        model = Liking
        fields = ['author', 'post_id']


class CommentFilter(FilterSet):
    post = filters.NumberFilter(field_name='post_id')

    class Meta:
        model = Comment
        fields = ['post']


class ProfileFilter(FilterSet):
    nickname = filters.CharFilter(field_name='nickname', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['nickname']


class FollowingViewSet(viewsets.ModelViewSet):
    serializer_class = FollowingSerializer
    queryset = Following.objects.all()
    permission_classes = [FollowingCheck]

    def perform_create(self, serializer):
        if self.request.data['following'] == self.request.data['follower']:
            raise exceptions.ValidationError(detail='자기 자신을 팔로우 할 수는 없습니다.')
        else:
            serializer.save()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [PostCheck]
    filter_backends = [DjangoFilterBackend]
    filter_class = PostFilter

    def perform_update(self, serializer):
        serializer.save(author_id=int(self.request.headers['userId']))


class LikingViewSet(viewsets.ModelViewSet):
    serializer_class = LikingSerializer
    queryset = Liking.objects.all()
    permission_classes = [LikingCheck]
    filter_backends = [DjangoFilterBackend]
    filter_class = LikingFilter

    def perform_create(self, serializer):
        post_id = self.request.data['post']
        user_id = self.request.data['user']
        check_like = Liking.objects.filter(post_id=post_id, user_id=user_id)
        if len(check_like) != 0:
            raise exceptions.ValidationError(detail='해당 유저는 이미 좋아요를 누른 상태입니다.')
        else:
            serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [CommentCheck]
    filter_backends = [DjangoFilterBackend]
    filter_class = CommentFilter


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [ProfileCheck]
    filter_backends = [DjangoFilterBackend]
    filter_class = ProfileFilter


# class ProfileDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             get_profile = Profile.objects.get(pk=pk)
#             serializer = ProfileSerializer(get_profile)
#             return JsonResponse(serializer.data)
#         except Profile.DoesNotExist:
#             return JsonResponse(status=404)
#
#
# class ProfileView(APIView):
#     def get(self):
#         profile_list = Profile.objects.all()
#         serializer = ProfileSerializer(profile_list, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     def post(self, request):
#         data = JSONParser().parse(request)
#         serializer = ProfileSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# class PostDetailView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Post, pk=pk)
#
#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return JsonResponse(serializer.data, status=200)
#
#     def put(self, request, pk):
#         user_id = request.headers["userId"]
#         data = JSONParser().parse(request)
#         get_post = self.get_object(pk)
#         serializer = PostSerializer(get_post, data=data)
#         # Validation 처리 과정
#         if serializer.is_valid():
#             if get_post.author_id != int(user_id):
#                 raise exceptions.AuthenticationFailed()
#             if get_post.author_id != data['author']:
#                 raise exceptions.ValidationError()
#             serializer.save()
#             return JsonResponse(serializer.data, status=201, safe=False)
#         return JsonResponse(serializer.errors, status=400, safe=False)
#
#     def delete(self, request, pk):
#         get_post = self.get_object(pk)
#         user_id = request.headers["userId"]
#         if get_post.author_id != int(user_id):
#             raise exceptions.AuthenticationFailed()
#         else:
#             get_post.delete()
#             return JsonResponse({"status": 204, "message": "SUCCESS"}, status=204, safe=False)
#
#
# class LikeView(APIView):
#     def post(self, request, pk):
#         get_post = get_object_or_404(Post, pk=pk)
#         user_id = int(request.headers["userId"])
#         query_set = {
#             'user': user_id,
#             'post': get_post.id,
#         }
#
#         liking = Liking.objects.filter(post_id=get_post.id, user_id=user_id)
#         if len(liking) > 0:
#             raise exceptions.ValidationError()
#
#         serializer = LikingSerializer(data=query_set)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({"status": 201, "message": "SUCCESS", 'data': serializer.data}, status=201, safe=False)
#         return JsonResponse(serializer.errors, status=400, safe=False)
#
#
#     def delete(self, request, pk):
#         get_post = get_object_or_404(Post, pk=pk)
#         user_id = int(request.headers["userId"])
#         query_set = Liking.objects.filter(post_id=get_post.id, user_id=user_id)
#         if len(query_set) is 0:
#             raise exceptions.ValidationError()
#         else:
#             query_set.delete()
#             return JsonResponse({"status": 204, "message": "SUCCESS"}, status=204, safe=False)
#
#
# class CommentView(APIView):
#     def post(self, request, pk):
#         get_post = get_object_or_404(Post, pk=pk)
#         user_id = request.headers["userId"]
#         script = request.data["script"]
#         query_set = {
#             'user': int(user_id),
#             'post': get_post.id,
#             'script': script
#         }
#         serializer = CommentSerializer(data=query_set)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({"status": 201, "message": "SUCCESS", "data": serializer.data}, status=201, safe=False)
#         return JsonResponse(serializer.errors, status=400, safe=False)
#
#
#     def delete(self, request, pk):
#         get_post = get_object_or_404(Post, pk=pk)
#         user_id = int(request.headers["userId"])
#         query_set = Comment.objects.filter(post_id=get_post.id, user_id=user_id)
#         if len(query_set) is 0:
#             raise exceptions.ValidationError()
#         else:
#             query_set.delete()
#             return JsonResponse({"status": 204, "message": "SUCCESS"}, status=204, safe=False)