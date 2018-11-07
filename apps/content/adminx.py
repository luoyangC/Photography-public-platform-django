"""
  Created by Amor on 2018-11-02
"""
import xadmin
from content.models import Topic, Activity, Agreement, Photo, Sample

__author__ = '骆杨'


class TopicAdmin(object):
    pass


class ActivityAdmin(object):
    pass


class AgreementAdmin(object):
    pass


class PhotoAdmin(object):
    pass


class SampleAdmin(object):
    pass


xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(Activity, ActivityAdmin)
xadmin.site.register(Agreement, AgreementAdmin)
xadmin.site.register(Photo, PhotoAdmin)
xadmin.site.register(Sample, SampleAdmin)
