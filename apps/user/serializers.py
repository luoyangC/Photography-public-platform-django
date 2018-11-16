"""
  Created by Amor on 2018-11-01
"""
import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import UserProfile, EmailVerifyRecord, Address

__author__ = '骆杨'


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, allow_blank=False, label='邮箱', help_text='邮箱',
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    code = serializers.CharField(max_length=6, min_length=6, write_only=True, label='验证码', help_text='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误'
                                 })
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='密码', help_text='密码')
    username = serializers.CharField(required=True, allow_blank=False, label='用户名', help_text='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all())])

    def validate_code(self, code):
        verify_records = EmailVerifyRecord.objects.filter(email=self.initial_data['email']).order_by('-create_time')
        if verify_records:
            last_record = verify_records[0]
            five_minutes_age = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_age > last_record.create_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        attrs['nick_name'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'email', 'code', 'password')


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('nick_name', 'birthday', 'gender', 'approve', 'email', 'mobile', 'image', 'id')


class EmailVerifySerializer(serializers.ModelSerializer):

    def validate_email(self, email):
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError('用户已存在')
        five_minutes_age = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=5, seconds=0)

        if EmailVerifyRecord.objects.filter(create_time__gt=five_minutes_age, email=email):
            raise serializers.ValidationError('距离上次发生不足5分钟，请查看邮件，或稍后再试')
        return email

    class Meta:
        model = EmailVerifyRecord
        fields = ('email', 'send_type')


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ('status', 'create_time')
