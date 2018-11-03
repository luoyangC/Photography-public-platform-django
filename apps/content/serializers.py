"""
  Created by Amor on 2018-11-02
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from content.models import Topic, Activity, Agreement

__author__ = '骆杨'

User = get_user_model()


class TopicSerializers(serializers.ModelSerializer):

    class Meta:
        model = Topic
        exclude = ('status', 'create_time')


class ActivitySerializers(serializers.ModelSerializer):

    class Meta:
        model = Activity
        exclude = ('status', 'create_time')


class AgreementSerializers(serializers.ModelSerializer):

    class Meta:
        model = Agreement
        exclude = ('status', 'create_time')
