from django.db import models

# Create your models here.


class Base(models.Model):
    """
    模型基础类
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.SmallIntegerField(default=1, verbose_name='状态')

    class Meta:
        abstract = True
