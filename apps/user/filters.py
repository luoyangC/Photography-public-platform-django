"""
  Created by Amor on 2018-11-24
"""
import django_filters
from user.models import UserProfile

__author__ = '骆杨'


class UserFilter(django_filters.rest_framework.FilterSet):
    """
    评论过滤器
    """
    self = django_filters.BooleanFilter(method='self_filter')

    def self_filter(self, queryset, name, value):
        user = self.request.user
        if value and isinstance(user, UserProfile):
            return UserProfile.objects.filter(id=user.id)
        return queryset.filter(id=0)

    class Meta:
        model = UserProfile
        fields = ['self', 'approve']
