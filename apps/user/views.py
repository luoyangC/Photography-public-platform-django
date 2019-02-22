from rest_framework import mixins, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from user.models import UserProfile, Address
from user.serializers import UserCreateSerializer, UserDetailSerializer, AddressSerializer, EmailVerifySerializer
from user.filters import UserFilter
from utils.email_send import send_email
from utils.weixin_create import get_weixin_user_info
from utils.permissions import IsSelfOrReadOnly

# Create your views here.


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 10


class UserViewSet(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserCreateSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    pagination_class = UserPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = UserFilter
    ordering_fields = ('update_time',)

    # 动态配置Serializer
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        return [IsSelfOrReadOnly()]


class EmailVerifyRecordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = EmailVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        send_email(email, send_type='register')
        return Response({'email': email}, status=status.HTTP_201_CREATED)


class AddressViewSet(viewsets.ModelViewSet):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class WeiXinView(APIView):
    """
    微信授权接口
    """
    def post(self, request):
        # 获取用户信息
        data = get_weixin_user_info(request.data)
        user = UserProfile.objects.filter(username=data['username']).first()

        # 判断用户是否存在，若不存在则创建用户
        if not user:
            user = UserProfile.objects.create(**data)

        # 生成用户token，返回给前端
        token = self.create_token(user)
        return Response({'token': token}, status=status.HTTP_200_OK)

    @staticmethod
    def create_token(user):
        # 生成用户token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token
