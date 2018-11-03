"""
  Created by Amor on 2018-11-03
"""
import xadmin
from xadmin import views

__author__ = '骆杨'


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '摄影公共平台'
    site_footer = '摄影公共平台'


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
