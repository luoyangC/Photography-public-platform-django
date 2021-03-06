"""
  Created by Amor on 2018-11-02
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from operate.models import Keep, Follow, Like, Comment, Reply, Message
from user.serializers import UserDetailSerializer
from content.serializers import ActivitySerializers, AgreementSerializers
from content.models import Topic

__author__ = '骆杨'


User = get_user_model()


class KeepSerializer(serializers.ModelSerializer):
    """
    收藏的序列化类
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Keep
        exclude = ('status', 'create_time')


class FollowSerializer(serializers.ModelSerializer):
    """
    关注的序列化类
    """
    follow = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class TopicSerializers(serializers.ModelSerializer):

        class Meta:
            model = Topic
            exclude = ('status', 'create_time')

    def get_follow(self, obj):
        if obj.follow_type == 'user':
            user = User.objects.filter(id=obj.follow_id).first()
            return UserDetailSerializer(user, context={'request': self.context['request']}).data
        elif obj.follow_type == 'topic':
            topic = Topic.objects.filter(id=obj.follow_id).first()
            return self.TopicSerializers(topic, context={'request': self.context['request']}).data
        else:
            return None

    class Meta:
        model = Follow
        exclude = ('status', 'create_time')


class LikeSerializer(serializers.ModelSerializer):
    """
    点赞的序列化类
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('id', 'user', 'activity')


class CommentSerializer(serializers.ModelSerializer):
    """
    评论的序列化类
    """
    is_author = serializers.SerializerMethodField()
    user = UserDetailSerializer(read_only=True)

    def validate(self, attrs):
        if attrs['activity'] and attrs['agreement']:
            raise serializers.ValidationError("activity or agreement only one")
        attrs['user'] = self.context['request'].user
        return attrs

    def get_is_author(self, obj):
        user = self.context['request'].user
        if isinstance(user, User):
            if user == obj.user:
                return True
        return False

    class Meta:
        model = Comment
        exclude = ('status',)


class CommentDetailSerializer(CommentSerializer):
    activity = ActivitySerializers()
    agreement = AgreementSerializers()


class ReplySerializer(serializers.ModelSerializer):
    """
    回复的序列化类
    """
    is_author = serializers.SerializerMethodField()
    to_user = UserDetailSerializer(read_only=True)
    from_user = UserDetailSerializer(read_only=True)

    def get_is_author(self, obj):
        user = self.context['request'].user
        if isinstance(user, User):
            if user == obj.from_user:
                return True
        return False

    def validate(self, attrs):
        if attrs['comment']:
            attrs['to_user'] = attrs['comment'].user
        if attrs['source_link']:
            attrs['to_user'] = attrs['source_link'].from_user
        attrs['from_user'] = self.context['request'].user
        return attrs

    class Meta:
        model = Reply
        exclude = ('status', )


class ReplayDetailSerializer(ReplySerializer):
    source_link = ReplySerializer()
    comment = CommentDetailSerializer()


class MessageSerializer(serializers.ModelSerializer):
    """
    消息的序列化类
    """
    read = serializers.BooleanField(read_only=True)
    # from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    from_user = UserDetailSerializer(read_only=True)

    def validate(self, attrs):
        if self.context['view'].action == 'create':
            if attrs['to_user'] == self.context['request'].user:
                raise serializers.ValidationError("to_user must not from_user")
            attrs['from_user'] = self.context['request'].user
            return attrs
        return attrs

    class Meta:
        model = Message
        exclude = ('status', )


class WebSocketMessageSerializer(serializers.ModelSerializer):
    """
    消息的序列化，用于websocket
    """
    class Meta:
        model = Message
        exclude = ('status', )
