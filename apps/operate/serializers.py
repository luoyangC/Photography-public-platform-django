"""
  Created by Amor on 2018-11-02
"""

from rest_framework import serializers

from operate.models import Keep, Follow, Like, Comment, Reply

__author__ = '骆杨'


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
        exclude = ('status', 'create_time')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ('status', 'create_time')


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        exclude = ('status', 'create_time')
