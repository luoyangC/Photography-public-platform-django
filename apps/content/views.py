from rest_framework import mixins, viewsets

from content.models import Topic, Activity, Agreement
from content.serializers import TopicSerializers, ActivitySerializers, AgreementSerializers

# Create your views here.


class TopicViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Topic.objects.all()
    serializer_class = TopicSerializers


class ActivityViewSet(viewsets.ModelViewSet):

    queryset = Activity.objects.all()
    serializer_class = ActivitySerializers


class AgreementViewSet(viewsets.ModelViewSet):

    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializers
