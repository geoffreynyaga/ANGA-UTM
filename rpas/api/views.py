from rpas.api.serializers import UserRPASListSerializer
from rpas.models import Rpas

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


class UserRPASListAPIView(ListAPIView):
    queryset = Rpas.objects.all()
    serializer_class = UserRPASListSerializer

    def get_queryset(self, *args, **kwargs):
        org = self.request.user.userprofile.organization
        queryset = Rpas.objects.filter(organization=org)
        return queryset

