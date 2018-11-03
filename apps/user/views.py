from rest_framework import mixins, viewsets

from user.models import UserProfile, EmailVerifyRecord, Address
from user.serializers import UserCreateSerializer, EmailVerifySerializer, AddressSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserCreateSerializer


class EmailVerifyRecordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = EmailVerifyRecord.objects.all()
    serializer_class = EmailVerifySerializer


class AddressViewSet(viewsets.ModelViewSet):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
