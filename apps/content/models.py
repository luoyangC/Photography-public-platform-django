from django.db import models
from basis.models import Base

from user.models import UserProfile, Address

# Create your models here.


class Content(Base):
    """
    内容基类
    """
    content = models.TextField(verbose_name='内容')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    like_nums = models.IntegerField(default=0, verbose_name='点赞数')
    comment_nums = models.IntegerField(default=0, verbose_name='评论数')

    class Meta:
        abstract = True


class Topic(Base):
    """
    主题
    """
    title = models.CharField(max_length=50, verbose_name='主题名称')
    info = models.CharField(max_length=500, verbose_name='主题描述')
    follow_nums = models.IntegerField(default=0, verbose_name='关注数')

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Photo(Base):
    """
    照片
    """
    image = models.ImageField(max_length=100, upload_to='image/content/%Y/%m', verbose_name='图片')
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='images', verbose_name='照片')

    class Meta:
        verbose_name = '照片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.activity.content


class Activity(Content):
    """
    动态
    """
    ACTIVITY_TYPE = (
        ('original', '原创'),
        ('forward', '转载'),
    )
    keep_nums = models.IntegerField(default=0, verbose_name='收藏数')
    share_nums = models.IntegerField(default=0, verbose_name='分享数')
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPE, verbose_name='动态类型')

    user = models.ForeignKey(UserProfile, related_name='contents', on_delete=models.CASCADE, verbose_name='作者')
    source_link = models.ForeignKey('self', null=True, blank=True, related_name='targets',
                                    on_delete=models.SET_NULL, verbose_name='转载来源')
    topic = models.ForeignKey(Topic, null=True, blank=True, related_name='contents',
                              on_delete=models.SET_NULL, verbose_name='主题')

    class Meta:
        verbose_name = '动态'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Agreement(Content):
    """
    约拍
    """
    AGREEMENT_TYPE = (
        ('free', '互免'),
        ('toll', '收费'),
        ('paid', '付费'),
    )
    agreement_type = models.CharField(max_length=5, choices=AGREEMENT_TYPE, verbose_name='约拍类型')
    amount = models.FloatField(default=0, verbose_name='金额')

    user = models.ForeignKey(UserProfile, related_name='agreements', on_delete=models.CASCADE, verbose_name='作者')
    address = models.ForeignKey(Address, related_name='agreements', on_delete=models.CASCADE, verbose_name='地址')

    class Meta:
        verbose_name = '约拍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
