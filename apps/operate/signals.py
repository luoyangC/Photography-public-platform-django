"""
  Created by Amor on 2018-12-04
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from operate.models import Message, Comment, Reply
from operate.consumers import new_message_notify


__author__ = '骆杨'


@receiver(post_save, sender=Message)
def create_message(sender, instance=None, created=False, **kwargs):
    if created:
        new_message_notify(instance)


@receiver(post_save, sender=Comment)
def create_comment(sender, instance=None, created=False, **kwargs):
    if created:
        message = Message()
        message.message_type = 'reply'
        message.comment = instance
        message.from_user = instance.user
        message.content = instance.content
        if instance.activity:
            message.to_user = instance.activity.user
        else:
            message.to_user = instance.agreement.user
        message.save()
        new_message_notify(message)


@receiver(post_save, sender=Reply)
def create_reply(sender, instance=None, created=False, **kwargs):
    if created:
        message = Message()
        message.message_type = 'reply'
        message.comment = instance.comment
        message.replay = instance
        message.to_user = instance.to_user
        message.from_user = instance.from_user
        message.content = instance.content
        message.save()
        new_message_notify(message)
