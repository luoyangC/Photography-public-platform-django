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
    content = models.TextField(verbose_name='回复内容')

    to_user = models.ForeignKey(UserProfile, related_name='reply_receives',
                                on_delete=models.CASCADE, verbose_name='接收者')
    from_user = models.ForeignKey(UserProfile, related_name='reply_sends',
                                  on_delete=models.CASCADE, verbose_name='发送者')
    comment = models.ForeignKey(Comment, related_name='replies',
                                on_delete=models.CASCADE, verbose_name='评论')
    source_link = models.ForeignKey('self', related_name='next', null=True, blank=True,
                                    on_delete=models.CASCADE, verbose_name='源回复')

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Like(Base):
    """
    用户点赞
    """
    activity = models.ForeignKey(Activity, related_name='likes', null=True, blank=True,
                                 on_delete=models.CASCADE, verbose_name='动态')
    user = models.ForeignKey(UserProfile, related_name='likes', on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nick_name


class Message(Base):
    """
    发起约拍
    """
    MESSAGE_TYPE = (
        ('letter', '私信'),
        ('invite', '邀请'),
        ('reply', '回复'),
        ('notice', '通知'),
    )
    ANSWER_TYPE = (
        (1, '未定义'),
        (2, '未回复'),
        (3, '同意'),
        (4, '拒绝'),
    )
    content = models.TextField(null=True, blank=True, verbose_name='内容')
    read = models.BooleanField(default=False, verbose_name='已读')
    answer = models.IntegerField(default=1, choices=ANSWER_TYPE, verbose_name='回答')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE, verbose_name='消息类型')

    agreement = models.ForeignKey(Agreement, related_name='messages', null=True, blank=True,
                                  on_delete=models.CASCADE, verbose_name='约拍')
    to_user = models.ForeignKey(UserProfile, related_name='message_receives',
                                on_delete=models.CASCADE, verbose_name='接收者')
    from_user = models.ForeignKey(UserProfile, related_name='message_sends',
                                  on_delete=models.CASCADE, verbose_name='发送者')

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
