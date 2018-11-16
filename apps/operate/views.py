from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from operate.models import Keep, Follow, Like, Comment, Reply
from operate.serializers import KeepSerializer, FollowSerializer, LikeSerializer
from operate.serializers import CommentSerializer, ReplySerializer, CommentDetailSerializer
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.


class MyViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """
    不提供Update方法
    """
    pass


class KeepViewSet(MyViewSet):

    queryset = Keep.objects.all()
    serializer_class = KeepSerializer


class FollowViewSet(MyViewSet):

    queryset = Follow.objects.all().order_by('-create_time')
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('user', 'follow_type')


class LikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

    permissions = IsOwnerOrReadOnly
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class CommentViewSet(MyViewSet):

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CommentDetailSerializer
        return CommentSerializer

    queryset = Comment.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReplyViewSet(MyViewSet):

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
