"""
  Created by Amor on 2018-12-03
"""

from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from operate import consumers

__author__ = '骆杨'


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('get/message/', consumers.MessageConsumer)
        ]),
    )
})
