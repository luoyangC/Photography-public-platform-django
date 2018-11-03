from rest_framework import mixins, viewsets

from operate.models import Keep, Follow, Like, Comment, Reply
from operate.serializers import KeepSerializer, FollowSerializer, LikeSerializer
from operate.serializers import CommentSerializer, ReplySerializer

# Create your views here.


class KeepViewSet(viewsets.ModelViewSet):

    queryset = Keep.objects.all()
    serializer_class = KeepSerializer


class FollowViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class LikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReplyViewSet(viewsets.ModelViewSet):

    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
