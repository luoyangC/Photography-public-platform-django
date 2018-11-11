from django.db import models

from basis.models import Base
from user.models import UserProfile
from content.models import Activity, Agreement

# Create your models here.


class Keep(Base):
    """
    用户收藏
    """
    activity = models.ForeignKey(Activity, related_name='keeps', on_delete=models.CASCADE, verbose_name='收藏的内容')
    user = models.ForeignKey(UserProfile, related_name='keeps', on_delete=models.CASCADE, verbose_name='收藏的用户')

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nick_name


class Follow(Base):
    """
    用户关注
    """
    FOLLOW_TYPE = (
        ('user', '用户'),
        ('topic', '主题')
    )
    follow_type = models.CharField(max_length=10, choices=FOLLOW_TYPE, verbose_name='关注类型')
    follow_id = models.IntegerField(verbose_name='关注id')

    user = models.ForeignKey(UserProfile, related_name='follows', on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        verbose_name = '关注'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nick_name


class Comment(Base):
    """
    用户评论
    """
    content = models.TextField(verbose_name='评论内容')

    agreement = models.ForeignKey(Agreement, null=True, blank=True, related_name='comments',
                                  on_delete=models.SET_NULL, verbose_name='评论的约拍')
    activity = models.ForeignKey(Activity, null=True, blank=True, related_name='comments',
                                 on_delete=models.SET_NULL, verbose_name='评论的动态')
    user = models.ForeignKey(UserProfile, related_name='comments', on_delete=models.CASCADE, verbose_name='评论者')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

    def get_reply_nums(self):
        return self.replies.count()


class Reply(Base):
    """
    用户回复
    """
    to_user_id = models.IntegerField(null=False, blank=False, verbose_name='接收者')
    content = models.TextField(verbose_name='回复内容')

    from_user = models.ForeignKey(UserProfile, related_name='replies', on_delete=models.CASCADE, verbose_name='发送者')
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE, verbose_name='评论')

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Like(Base):
    """
    用户点赞
    """
    activity = models.ForeignKey(Activity, related_name='likes', on_delete=models.CASCADE, verbose_name='动态')
    user = models.ForeignKey(UserProfile, related_name='likes', on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nick_name


class Send(Base):
    """
    发起约拍
    """
    content = models.TextField(verbose_name='内容')
    answer = models.BooleanField(default=False, verbose_name='回答')

    agreement = models.ForeignKey(Agreement, related_name='sends', on_delete=models.CASCADE, verbose_name='约拍')
    user = models.ForeignKey(UserProfile, related_name='sends', on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        verbose_name = '发起'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
