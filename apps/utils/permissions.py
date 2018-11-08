"""
  Created by Amor on 2018-11-08
"""

from rest_framework import permissions

__author__ = '骆杨'


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
