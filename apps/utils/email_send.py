"""
  Created by Amor on 2018-11-11
"""
import random

from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from photography.settings import EMAIL_FROM

__author__ = '骆杨'


def send_email(email, send_type='register'):
    code = make_random_code(email)
    if send_type == 'register':
        email_title = 'photography注册激活码'
        text_content = """
                        感谢注册www.photography.com!\
                        您的注册验证码为{}，请在规定时间内完成注册验证
                       """.format(code)
        html_content = """
                        <h3>感谢注册<a href='http://www.luoyangc.com'>我的个人主页</a></p>\
                        <p>您的邮箱验证码为{}，请在规定时间内完成注册</p>
                       """.format(code)
        msg = EmailMultiAlternatives(email_title, text_content, EMAIL_FROM, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


def make_random_code(email):
    code = random.randint(100000, 999999)
    cache.set(email, code, timeout=60 * 5)
    return code
