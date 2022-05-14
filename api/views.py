import django_filters

from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend\



class ProfileFilter(django_filters.FilterSet):
    nickname = django_filters.CharFilter(field_name='nickname', lookup_expr="contains")
    image = django_filters.BooleanFilter(field_name="profileImg", method='filter_image')

    class Meta:
        model = Profile
        fields = ['nickname', 'profileImg']

    def filter_image(self,queryset, profileImg , value):
        if value:
            return queryset.filter(profileImg__isnull=True)
        else:
            return queryset.filter(profile__isnull=False)


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfileFilter
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]








