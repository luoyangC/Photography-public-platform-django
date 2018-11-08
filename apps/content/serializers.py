"""
  Created by Amor on 2018-11-02
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from content.models import Topic, Activity, Agreement, Photo, Sample
from user.serializers import UserDetailSerializer, AddressSerializer
from operate.serializers import CommentSerializer

__author__ = '骆杨'

User = get_user_model()


class PhotoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('image', )


class SampleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Sample
        fields = ('image',)


class TopicSerializers(serializers.ModelSerializer):

    class Meta:
        model = Topic
        exclude = ('status', 'create_time')


class ActivitySerializers(serializers.ModelSerializer):

    topic = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    keep_nums = serializers.SerializerMethodField()
    comment_nums = serializers.SerializerMethodField()
    like_nums = serializers.SerializerMethodField()
    share_nums = serializers.SerializerMethodField()

    images = PhotoSerializers(many=True, read_only=True)

    @staticmethod
    def get_comment_nums(obj):
        comment_nums = obj.comments.count()
        return comment_nums

    @staticmethod
    def get_like_nums(obj):
        like_nums = obj.likes.count()
        return like_nums

    @staticmethod
    def get_keep_nums(obj):
        keep_nums = obj.keeps.count()
        return keep_nums

    @staticmethod
    def get_share_nums(obj):
        share_nums = obj.targets.count()
        return share_nums

    def get_source(self, obj):

        if obj.source_link is None:
            return None
        else:
            original = obj.get_original()
            source = ActivitySerializers(original, context={'request': self.context['request']})
            return source.data

    def get_topic(self, obj):
        topic = TopicSerializers(obj.topic, context={'request': self.context['request']})
        return topic.data

    def get_user(self, obj):
        user = UserDetailSerializer(obj.user, context={'request': self.context['request']})
        return user.data

    def get_is_author(self, obj):
        user = self.context['request'].user
        if user == obj.user:
            return True
        return False

    class Meta:
        model = Activity
        exclude = ('status', 'source_link')


class ActivityDetailSerializers(ActivitySerializers):

    comments = CommentSerializer(many=True, read_only=True)


class ActivityCreateSerializers(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['activity_type'] == 'forward' and not attrs['source_link']:
            raise serializers.ValidationError("if forward, source_link is must")
        elif attrs['activity_type'] == 'original' and attrs['source_link']:
            raise serializers.ValidationError("if original, source_link must not")
        return attrs

    class Meta:
        model = Activity
        exclude = ('status',)


class AgreementSerializers(serializers.ModelSerializer):

    images = SampleSerializers(many=True, read_only=True)

    user = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    comment_nums = serializers.SerializerMethodField()
    send_nums = serializers.SerializerMethodField()

    @staticmethod
    def get_comment_nums(obj):
        comment_nums = obj.comments.count()
        return comment_nums

    @staticmethod
    def get_send_nums(obj):
        send_nums = obj.sends.count()
        return send_nums

    def get_user(self, obj):
        user = UserDetailSerializer(obj.user, context={'request': self.context['request']})
        return user.data

    def get_address(self, obj):
        address = AddressSerializer(obj.address, context={'request': self.context['request']})
        return address.data

    class Meta:
        model = Agreement
        exclude = ('status', )


class AgreementDetailSerializer(AgreementSerializers):
    comments = CommentSerializer(many=True, read_only=True)


class AgreementCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Agreement
        exclude = ('status',)
