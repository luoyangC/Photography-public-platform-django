from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from operate.models import Keep, Follow, Like, Comment, Reply, Message
from operate.filters import CommentFilter, ReplyFilter, MessageFilter
from operate.serializers import KeepSerializer, FollowSerializer, LikeSerializer, ReplayDetailSerializer
from operate.serializers import CommentSerializer, ReplySerializer, MessageSerializer, CommentDetailSerializer
from utils.permissions import IsOwnerOrReadOnly, IsFromOrReadOnly, IsToOrReadOnly

# Create your views here.


class KeepViewSet(viewsets.ModelViewSet):

    # 验证和权限
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permissions = IsOwnerOrReadOnly

    # 模型和序列化
    def get_queryset(self):
        queryset = Keep.objects.filter(user=self.request.user)
        return queryset
    serializer_class = KeepSerializer


class FollowViewSet(viewsets.ModelViewSet):

    # 验证和权限
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permissions = IsOwnerOrReadOnly

    # 模型和序列化
    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset
    serializer_class = FollowSerializer

    # 查询和过滤
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'follow_type')


class LikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    # 验证和权限
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permissions = IsOwnerOrReadOnly

    # 模型和序列化
    def get_queryset(self):
        queryset = Like.objects.filter(user=self.request.user)
        return queryset
    serializer_class = LikeSerializer


class CommentViewSet(viewsets.ModelViewSet):

    # 验证和权限
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 模型和序列化
    def get_serializer_class(self):
        is_detail = self.request.query_params.get('is_detail')
        if is_detail == '2' or is_detail == 2:
            return CommentDetailSerializer
        return CommentSerializer
    queryset = Comment.objects.all()

    # 查询和过滤、排序
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = CommentFilter
    ordering_fields = ('update_time',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReplyViewSet(viewsets.ModelViewSet):

    # 验证和权限
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsFromOrReadOnly()]
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 模型和序列化
    def get_serializer_class(self):
        is_detail = self.request.query_params.get('is_detail')
        if is_detail == '2' or is_detail == 2:
            return ReplayDetailSerializer
        return ReplySerializer
    queryset = Reply.objects.all()

    # 查询和过滤、排序
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ReplyFilter
    ordering_fields = ('update_time',)


class MessageViewSet(viewsets.ModelViewSet):

    # 验证和权限
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action == 'update' or 'partial_update':
            return [IsToOrReadOnly()]
        return [IsFromOrReadOnly()]
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 模型和序列化
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    # 查询和过滤
    filter_backends = (DjangoFilterBackend, )
    filter_class = MessageFilter
