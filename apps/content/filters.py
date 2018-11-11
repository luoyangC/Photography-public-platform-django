"""
  Created by Amor on 2018-11-08
"""
import django_filters
from content.models import Activity

__author__ = '骆杨'


class ActivityFilter(django_filters.rest_framework.FilterSet):
    """
    动态过滤器
    """

    class Meta:
        model = Activity
        fields = ['topic', 'activity_type']
