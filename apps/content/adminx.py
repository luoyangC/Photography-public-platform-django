"""
  Created by Amor on 2018-11-02
"""
import xadmin
from content.models import Topic, Activity, Agreement

__author__ = '骆杨'


class TopicAdmin(object):
    pass


class ActivityAdmin(object):
    pass


class AgreementAdmin(object):
    pass


xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(Activity, ActivityAdmin)
xadmin.site.register(Agreement, AgreementAdmin)
