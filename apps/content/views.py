from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from content.models import Topic, Activity, Agreement, Photo, Sample
from content.serializers import TopicSerializers, ActivitySerializers, AgreementSerializers
from content.serializers import ActivityCreateSerializers, AgreementCreateSerializers, SampleSerializers
from content.serializers import PhotoCreateSerializers, SampleCreateSerializers
from content.serializers import PhotoSerializers
from content.filters import ActivityFilter
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.


class PhotoViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return PhotoCreateSerializers
        return PhotoSerializers

    queryset = Photo.objects.all()


class SampleViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return SampleCreateSerializers
        return SampleSerializers

    queryset = Sample.objects.all()


class TopicViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Topic.objects.all()
    serializer_class = TopicSerializers
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = (SearchFilter,)
    search_fields = ('title', )


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
        return ActivitySerializers

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    queryset = Activity.objects.all().order_by('-update_time')
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ActivityFilter
    ordering_fields = ('update_time', 'like_nums')


class AgreementViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return AgreementCreateSerializers
        return AgreementSerializers

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    queryset = Agreement.objects.all().order_by('-update_time')
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    filter_backends = (SearchFilter,)
    search_fields = ('content', 'address')
