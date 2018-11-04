"""
  Created by Amor on 2018-11-04
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

__author__ = '骆杨'


User = get_user_model()


@receiver(post_save, sender=User)
def create_auth(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
