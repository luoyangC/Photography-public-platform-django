from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from content.models import Topic, Activity, Agreement
from content.serializers import TopicSerializers, ActivitySerializers, AgreementSerializers

# Create your views here.


class TopicViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Topic.objects.all()
    serializer_class = TopicSerializers


class ActivityViewSet(viewsets.ModelViewSet):

    queryset = Activity.objects.all()
    serializer_class = ActivitySerializers
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class AgreementViewSet(viewsets.ModelViewSet):

    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializers
