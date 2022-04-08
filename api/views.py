from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import *
from api.serializers import *
from rest_framework import viewsets

@csrf_exempt
def post_api(request):
    if request.method == 'GET':
        post_list = Post.objects.all()
        serializer = PostSerializer(post_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def post_detail(request, pk):
    try:
        get_post = Post.objects.get(pk=pk)
        serializer = PostSerializer(get_post)
        return JsonResponse(serializer.data)
    except Post.DoesNotExist:
        return JsonResponse(status=404)


@csrf_exempt
def profile_api(request):
    if request.method == 'GET':
        profile_list = Profile.objects.all()
        serializer = ProfileSerializer(profile_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def profile_detail(request, pk):
    try:
        get_profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(get_profile)
        return JsonResponse(serializer.data)
    except Profile.DoesNotExist:
        return JsonResponse(status=404)

