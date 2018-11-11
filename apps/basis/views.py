from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# Create your views here.
from user.models import UserProfile


class CustomBackend(ModelBackend):
    """验证用户 让用户可以使用邮箱登陆"""

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 做并集进行查询  使用Q
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 先查user 然后调用方法去比较密码
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
            return None
