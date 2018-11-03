from django.db import models
from django.contrib.auth.models import AbstractUser

from basis.models import Base

# Create your models here.


class UserProfile(AbstractUser, Base):
    """
    用户信息
    """
    GENDER_TYPE = (
        ('male', '男'),
        ('female', '女'),
        ('unknown', '未知'),
    )
    USER_TYPE = (
        ('photographer', '摄影师'),
        ('model', '模特'),
        ('general', '普通用户'),
    )
    nick_name = models.CharField(max_length=10, null=True, blank=True, verbose_name='昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    gender = models.CharField(max_length=8, choices=GENDER_TYPE, default='unknown', verbose_name='性别')
    approve = models.CharField(max_length=12, choices=USER_TYPE, default='general', verbose_name='认证类型')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='电话')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='邮箱')
    image = models.ImageField(max_length=100, upload_to='image/user/%Y/%m',
                              default='image/user/default/1.png', verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Address(Base):
    """
    地址
    """
    province = models.CharField(max_length=50, verbose_name='省')
    city = models.CharField(max_length=50, verbose_name='市')
    district = models.CharField(max_length=50, verbose_name='区县')
    addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='详细地址')

    user = models.ForeignKey('UserProfile', related_name='addresses', on_delete=models.CASCADE, verbose_name='用户地址')

    class Meta:
        verbose_name = '地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}-{}-{}'.format(self.province, self.city, self.district)


class EmailVerifyRecord(Base):
    """
    邮箱验证
    """
    SEND_TYPE = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update', '修改邮箱')
    )
    code = models.CharField(max_length=100, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=10, choices=SEND_TYPE, verbose_name='验证码类型')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email
