from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.models import UserProfile, EmailVerifyRecord, Address
from user.serializers import UserCreateSerializer, EmailVerifySerializer, AddressSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated, )
    queryset = UserProfile.objects.all()
    serializer_class = UserCreateSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class EmailVerifyRecordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = EmailVerifyRecord.objects.all()
    serializer_class = EmailVerifySerializer


class AddressViewSet(viewsets.ModelViewSet):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
