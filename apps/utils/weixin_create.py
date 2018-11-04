"""
  Created by Amor on 2018-11-04
"""
import random
import string

from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt
from weixin.oauth2 import OAuth2AuthExchangeError

from photography.settings import APP_ID
from photography.settings import APP_SECRET

__author__ = '骆杨'


# 获取微信用户信息
def get_weixin_user_info(data):

    # 获取前端传递过来的三个关键的值
    code = data['code']
    iv = data['detail']['iv']
    encrypted_data = data['detail']['encryptedData']

    # 用配置文件中的配置生成API接口
    api = WXAPPAPI(appid=APP_ID, app_secret=APP_SECRET)
    try:
        # 使用code换取session_key
        session_info = api.exchange_code_for_session_key(code)
    except OAuth2AuthExchangeError as e:
        print(e, '验证失败，请重试')
    session_key = session_info.get('session_key')

    # 使用session_key生成密钥
    crypt = WXBizDataCrypt(APP_ID, session_key)
    try:
        # 解密得到用户信息
        user_info = crypt.decrypt(encrypted_data, iv)
    except UnicodeDecodeError as e:
        print(e, '请从新获取用户授权')

    _data = format_user_info(user_info)

    return _data


# 格式化用户信息
def format_user_info(user_info):
    data = {
        'username': user_info['openId'],
        'nick_name': user_info['nickName'],
        'gender': user_info['gender'],
        'image': user_info['avatarUrl'],
        'password': make_ran_str()
    }
    return data


# 生成随机密码
def make_ran_str():
    return ''.join(random.sample(string.ascii_letters + string.digits, 12))
