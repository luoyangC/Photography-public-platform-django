"""
  Created by Amor on 2018-12-03
"""

from django.core.cache import cache
from rest_framework_jwt.utils import jwt_decode_handler
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from user.models import UserProfile
from operate.models import Message
from operate.serializers import WebSocketMessageSerializer

__author__ = '骆杨'

channel_layer = get_channel_layer()


def make_headers(req):
    # 解析请求头，返回一个字典格式，这么写主要是因为里面的内容需要解码
    headers = {}
    for item in req:
        headers[item[0].decode('utf-8')] = item[1].decode('utf-8')
    return headers


def token_get_user(token):
    # 解析JWT获取User对象
    user = jwt_decode_handler(token)
    return user


@database_sync_to_async
def get_message(user_id):
    # 通过用户ID获取到用户的未读消息，并返回序列化数据
    messages = Message.objects.filter(to_user_id=user_id, read=False)
    return messages


def new_message_notify(instance):
    # 创建新消息时，发送一个推送消息
    channel_name = cache.get(instance.to_user_id)
    if channel_name:
        message = WebSocketMessageSerializer(instance).data
        async_to_sync(channel_layer.send)(channel_name, {
            "type": "push.message",
            "data": message,
        })


class MessageConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = make_headers(self.scope['headers'])
        self.user = token_get_user(self.headers['authorization'])

    async def connect(self):
        # 建立WebSocket连接的时候调用该方法
        user = UserProfile.objects.filter(id=self.user['user_id']).first()
        if user:
            # todo: 消息推送有点问题
            messages = await get_message(user.id)
            await self.accept()
            await self.send_json([{'hello': 'word'}])
            cache.set(self.user['user_id'], self.channel_name, timeout=None)
        else:
            await self.close()

    async def disconnect(self, close_code):
        # 连接关闭后调用该方法
        await self.close()
        cache.delete_pattern(self.user['user_id'])

    async def push_message(self, event):
        # 推送消息
        message = event['data']
        await self.send_json(message)
