"""
  Created by Amor on 2018-11-02
"""
import xadmin

from operate.models import Keep, Follow, Like, Comment, Reply

__author__ = '骆杨'


class KeepAdmin(object):
    pass


class FollowAdmin(object):
    pass


class LikeAdmin(object):
    pass


class CommentAdmin(object):
    pass


class ReplyAdmin(object):
    pass


xadmin.site.register(Keep, KeepAdmin)
xadmin.site.register(Follow, FollowAdmin)
xadmin.site.register(Like, LikeAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Reply, ReplyAdmin)
