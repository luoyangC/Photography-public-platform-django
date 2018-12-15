"""
  Created by Amor on 2018-11-08
"""
import django_filters
from content.models import Activity
from operate.models import Follow, Keep
from user.models import UserProfile

__author__ = '骆杨'


class ActivityFilter(django_filters.rest_framework.FilterSet):
    """
    动态过滤器
    """
    follow = django_filters.CharFilter(method='follow_filter', label='关注')
    keep = django_filters.BooleanFilter(method='keep_filter', label='收藏')

    def follow_filter(self, queryset, name, value):
        follow_type = value
        user = self.request.user
        if isinstance(user, UserProfile) and follow_type == 'user':
            follow_list = Follow.objects.filter(user=user, follow_type=follow_type)
            follow_list = [i.follow_id for i in follow_list]
            follow_list.append(user.id)
            queryset = queryset.filter(user_id__in=follow_list)
            return queryset
        elif isinstance(user, UserProfile) and follow_type == 'topic':
            follow_list = Follow.objects.filter(user=user, follow_type=follow_type)
            follow_list = [i.follow_id for i in follow_list]
            queryset = queryset.filter(topic_id__in=follow_list)
            return queryset
        else:
            return queryset

    def keep_filter(self, queryset, name, value):
        user = self.request.user
        if isinstance(user, UserProfile) and value:
            keep_list = Keep.objects.filter(user=user)
            keep_list = [i.activity_id for i in keep_list]
            queryset = queryset.filter(id__in=keep_list)
            return queryset
        return queryset

    class Meta:
        model = Activity
        fields = ['topic', 'activity_type', 'user', 'follow', 'keep']
