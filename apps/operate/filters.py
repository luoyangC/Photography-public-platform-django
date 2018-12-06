"""
  Created by Amor on 2018-11-20
"""
import django_filters
from django.db.models import Q

from operate.models import Comment, Reply, Message
from user.models import UserProfile
from content.models import Agreement

__author__ = '骆杨'


class CommentFilter(django_filters.rest_framework.FilterSet):
    """
    评论过滤器
    """
    class Meta:
        model = Comment
        fields = ['activity', 'user', 'agreement']


class ReplyFilter(django_filters.rest_framework.FilterSet):
    """
    回复过滤器
    """
    class Meta:
        model = Reply
        fields = ['comment', 'from_user']


class MessageFilter(django_filters.rest_framework.FilterSet):
    """
    消息过滤器
    """
    agreement = django_filters.NumberFilter(method='agreement_filter', label='约拍')
    is_from = django_filters.BooleanFilter(method='is_from_filter', label='是发送者')
    is_to = django_filters.BooleanFilter(method='is_to_filter', label='是接收者')
    other = django_filters.NumberFilter(method='other_filter', label='对方')

    def other_filter(self, queryset, name, value):
        current_user = self.request.user
        other_user = UserProfile.objects.filter(id=value).first()
        if isinstance(current_user, UserProfile) and other_user:
            read_queryset = queryset.filter(Q(from_user_id=current_user.id, to_user_id=other_user.id) |
                                            Q(from_user_id=other_user.id, to_user_id=current_user.id, read=True))
            not_read_queryset = queryset.filter(from_user_id=other_user.id, to_user_id=current_user.id, read=False)
            not_read_queryset.update(read=True)
            read_nums = read_queryset.count()
            not_read_nums = not_read_queryset.count()
            if not_read_nums > 20:
                return not_read_queryset
            elif not_read_nums + read_nums < 20:
                return not_read_queryset.union(not_read_queryset, read_queryset)
            else:
                delta = 20 - not_read_nums
                return not_read_queryset.union(not_read_queryset, read_queryset[:delta])
        return queryset.none()

    def is_from_filter(self, queryset, name, value):
        current_user = self.request.user
        if isinstance(current_user, UserProfile):
            if value:
                queryset = queryset.filter(from_user=current_user)
                return queryset
            else:
                queryset = queryset.exclude(from_user=current_user)
                return queryset
        return queryset

    def is_to_filter(self, queryset, name, value):
        current_user = self.request.user
        if isinstance(current_user, UserProfile):
            if value:
                queryset = queryset.filter(to_user_id=current_user.id)
                return queryset
            else:
                queryset = queryset.exclude(to_user_id=current_user.id)
                return queryset
        return queryset

    def agreement_filter(self, queryset, name, value):
        current_user = self.request.user
        if isinstance(current_user, UserProfile):
            agreement = Agreement.objects.filter(id=value).first()
            queryset = queryset.filter(agreement=value)
            if agreement.user == current_user:
                return queryset
            else:
                return queryset.filter(from_user=current_user)
        return queryset.filter(from_user=0)

    class Meta:
        model = Message
        fields = ['agreement', 'message_type', 'read', 'is_from', 'is_to', 'other']
