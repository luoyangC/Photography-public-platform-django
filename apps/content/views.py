from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from content.models import Topic, Activity, Agreement
from content.serializers import TopicSerializers, ActivitySerializers, AgreementSerializers, ActivityDetailSerializers
from content.serializers import ActivityCreateSerializers, AgreementCreateSerializers, AgreementDetailSerializer
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.


class TopicViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Topic.objects.all()
    serializer_class = TopicSerializers


class ActivityViewSet(viewsets.ModelViewSet):
    """
    list: 动态列表
    create: 添加一个动态
    update: 更新一个动态
    delete: 删除一个动态
    retrieve: 查看动态详情
    """
    def get_serializer_class(self):
        if self.action == 'create':
            return ActivityCreateSerializers
        elif self.action == 'retrieve':
            return ActivityDetailSerializers
        return ActivitySerializers

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    queryset = Activity.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class AgreementViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return AgreementCreateSerializers
        elif self.action == 'retrieve':
            return AgreementDetailSerializer
        return AgreementSerializers

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    queryset = Agreement.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
