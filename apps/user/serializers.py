"""
  Created by Amor on 2018-11-01
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import UserProfile, EmailVerifyRecord, Address

__author__ = '骆杨'


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('username', 'email')


class EmailVerifySerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailVerifyRecord
        fields = ('email', 'send_type')


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ('status', 'create_time')
