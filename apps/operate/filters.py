"""
  Created by Amor on 2018-11-20
"""
import django_filters
from operate.models import Comment

__author__ = '骆杨'


class CommentFilter(django_filters.rest_framework.FilterSet):
    """
    评论过滤器
    """
    class Meta:
        model = Comment
        fields = ['activity', 'user']
