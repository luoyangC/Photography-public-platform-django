from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from operate.models import Keep, Follow, Like, Comment, Reply
from operate.filters import CommentFilter, ReplyFilter
from operate.serializers import KeepSerializer, FollowSerializer, LikeSerializer
from operate.serializers import CommentSerializer, ReplySerializer
from utils.permissions import IsOwnerOrReadOnly, IsFromOrReadOnly

# Create your views here.


class KeepViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Keep.objects.filter(user=self.request.user)
        return queryset
    serializer_class = KeepSerializer
    permissions = IsOwnerOrReadOnly
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class FollowViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset
    serializer_class = FollowSerializer
    permissions = IsOwnerOrReadOnly
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('user', 'follow_type')


class LikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        queryset = Like.objects.filter(user=self.request.user)
        return queryset
    permissions = IsOwnerOrReadOnly
    serializer_class = LikeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class CommentViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = CommentFilter
    ordering_fields = ('update_time',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReplyViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsFromOrReadOnly()]

    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ReplyFilter
    ordering_fields = ('update_time',)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
