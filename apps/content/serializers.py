"""
  Created by Amor on 2018-11-02
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from content.models import Topic, Activity, Agreement, Photo, Sample
from user.serializers import UserDetailSerializer, AddressSerializer

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
    is_author = serializers.SerializerMethodField()

    images = PhotoSerializers(many=True)

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
        exclude = ('status', )


class AgreementSerializers(serializers.ModelSerializer):

    images = SampleSerializers(many=True)

    user = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = UserDetailSerializer(obj.user, context={'request': self.context['request']})
        return user.data

    def get_address(self, obj):
        address = AddressSerializer(obj.address, context={'request': self.context['request']})
        return address.data

    class Meta:
        model = Agreement
        exclude = ('status', )
