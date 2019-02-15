"""
  Created by Amor on 2018-11-02
"""

import xadmin
from django.contrib.auth import get_user_model

from user.models import Address

__author__ = '骆杨'


User = get_user_model()


class UserAdmin(object):
    model_icon = 'fa fa-user'


class AddressAdmin(object):
    pass


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
xadmin.site.register(Address, AddressAdmin)
