from api.models import *
from api.serializers import *
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

from django.utils import timezone
import datetime
import pytz


class PostFilter(FilterSet):
	user = filters.NumberFilter(field_name='user')
	is_recently_modified = filters.BooleanFilter(method='filter_is_recently_modified')

	class Meta:
		model = Post
		fields = '__all__'

	def filter_is_recently_modified(self, queryset, name, value):
		end_date = timezone.localtime(timezone.now()).replace(tzinfo=pytz.timezone('Asia/Seoul'))
		start_date = end_date + datetime.timedelta(-6)	# 최근 6시간 이내에 수정된 포스트

		return queryset.filter(modified_at__range=(start_date, end_date))

class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()
	filter_backends = [DjangoFilterBackend]
	filterset_class = PostFilter