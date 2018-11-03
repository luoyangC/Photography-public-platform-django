"""
    photography URL Configuration
"""
import xadmin
from django.urls import path, include
from django.views.static import serve
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from photography.settings import MEDIA_ROOT
from user import views as user_views
from content import views as content_views
from operate import views as operate_views


router = DefaultRouter()


# 用户接口
router.register('user', user_views.UserViewSet, base_name='user')
# 邮件接口
router.register('code', user_views.EmailVerifyRecordViewSet, base_name='code')
# 地址接口
router.register('address', user_views.AddressViewSet, base_name='address')
# 主题接口
router.register('topic', content_views.TopicViewSet, base_name='topic')
# 动态接口
router.register('activity', content_views.ActivityViewSet, base_name='activity')
# 约拍接口
router.register('agreement', content_views.AgreementViewSet, base_name='agreement')
# 收藏接口
router.register('keep', operate_views.KeepViewSet, base_name='keep')
# 关注接口
router.register('follow', operate_views.FollowViewSet, base_name='follow')
# 点赞接口
router.register('like', operate_views.LikeViewSet, base_name='like')
# 评论接口
router.register('comment', operate_views.CommentViewSet, base_name='comment')
# 回复接口
router.register('reply', operate_views.ReplyViewSet, base_name='reply')


urlpatterns = [
    # 主页地址
    path('', RedirectView.as_view(url='api/')),
    # 后台管理
    path('admin/', xadmin.site.urls),
    # 站点图标
    path('favicon.ico', RedirectView.as_view(url='static/favicon.ico')),
    # 媒体文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # DRF登录
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # DRF文档
    path('docs/', include_docs_urls(title='文档')),
    # 获取授权
    path('api/login/', obtain_jwt_token),
    # API入口
    path('api/', include(router.urls)),
]
