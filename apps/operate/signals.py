"""
  Created by Amor on 2018-12-04
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from operate.models import Message
from operate.consumers import new_message_notify


__author__ = '骆杨'


@receiver(post_save, sender=Message)
def create_auth(sender, instance=None, created=False, **kwargs):
    if created:
        new_message_notify(instance)
