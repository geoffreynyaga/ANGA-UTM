from rpas.models import RpasModel
from rpas.api.serializers import UserRPASListSerializer, UserRPASModelListSerializer
from rpas.models import Rpas, RpasModel

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


class UserRPASListAPIView(ListAPIView):
    queryset = Rpas.objects.all()
    serializer_class = UserRPASListSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self, *args, **kwargs):
        org = self.request.user.userprofile.organization
        queryset = Rpas.objects.filter(organization=org)
        return queryset


class UserRPASModelsListAPIView(ListAPIView):
    queryset = RpasModel.objects.all()
    serializer_class = UserRPASModelListSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self, *args, **kwargs):
        queryset = RpasModel.objects.all()
        return queryset
