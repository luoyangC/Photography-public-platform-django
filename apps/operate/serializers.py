"""
  Created by Amor on 2018-11-02
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from operate.models import Keep, Follow, Like, Comment, Reply
from user.serializers import UserDetailSerializer

__author__ = '骆杨'


User = get_user_model()


class KeepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keep
        exclude = ('status', 'create_time')


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        exclude = ('status', 'create_time')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'activity')


class ReplySerializer(serializers.ModelSerializer):

    from_user = UserDetailSerializer()
    to_user = serializers.SerializerMethodField()

    def get_to_user(self, obj):
        user = User.objects.filter(id=obj.to_user_id)[0]
        to_user_serializer = UserDetailSerializer(user, context={'request': self.context['request']})
        return to_user_serializer.data

    class Meta:
        model = Reply
        exclude = ('status', 'create_time', 'to_user_id', 'comment')


class CommentSerializer(serializers.ModelSerializer):

    replies = ReplySerializer(many=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ('status', 'create_time', 'agreement', 'activity')
