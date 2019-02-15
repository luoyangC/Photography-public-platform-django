"""
  Created by Amor on 2018-11-01
"""
from django.core.cache import cache

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import UserProfile, Address
from operate.models import Follow

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
        verify_records = cache.get(self.initial_data['email'])
        if verify_records:
            if verify_records != code:
                raise serializers.ValidationError('验证码错误')
            else:
                return code
        else:
            raise serializers.ValidationError('验证码过期')

    def validate(self, attrs):
        attrs['nick_name'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'email', 'code', 'password')


class UserDetailSerializer(serializers.ModelSerializer):

    follow_nums = serializers.SerializerMethodField()
    is_follow = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.image.url + '/avatar'

    def get_follow_nums(self, obj):
        user = self.context['request'].user
        if isinstance(user, User):
            follow_nums = Follow.objects.filter(follow_type='user', follow_id=obj.id).count()
            if follow_nums:
                return follow_nums
        return False

    def get_is_follow(self, obj):
        user = self.context['request'].user
        if isinstance(user, User):
            follow = Follow.objects.filter(user=user, follow_type='user', follow_id=obj.id).first()
            if follow:
                return follow.id
        return False

    class Meta:
        model = UserProfile
        fields = ('nick_name', 'birthday', 'gender', 'approve',
                  'email', 'mobile', 'image', 'id', 'simple_info',
                  'is_follow', 'follow_nums')


class EmailVerifySerializer(serializers.Serializer):

    email = serializers.EmailField()
    send_type = serializers.CharField()

    def validate(self, attrs):
        if attrs['send_type'] == 'register':
            if User.objects.filter(email=attrs['email']).count():
                raise serializers.ValidationError('用户已存在')
        if cache.get('email'):
            raise serializers.ValidationError('距离上次发生不足5分钟，请查看邮件，或稍后再试')
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ('status', 'create_time')
