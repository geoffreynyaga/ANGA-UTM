from rpas.models import Rpas
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate as django_authenticate,
)
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, serializers, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveAPIView


from rest_framework.authentication import TokenAuthentication


from accounts.api.serializers import (
    SignupSerializer,
    UserProfileDetailSerializer,
    UserProfileFlightLogSerializer,
    UserProfileUASListSerializer,
)
from accounts.models import UserProfile

from applications.models import ReserveAirspace
from accounts.api.serializers import LoginSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import serializers, exceptions


from django.core.exceptions import ValidationError


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileDetailSerializer
    lookup_field = "pk"
    queryset = UserProfile.objects.all()


class UserProfileFlightLogsListAPIView(generics.ListAPIView):
    serializer_class = UserProfileFlightLogSerializer

    def get_queryset(self):
        """
        This view should return a list of all the logs
        for the currently authenticated user.
        """

        try:
            url_pk = self.kwargs.get("pk")
            user_from_url = User.objects.get(pk=url_pk)
            if user_from_url == self.request.user:

                queryset = ReserveAirspace.objects.filter(
                    created_by=self.request.user
                ).order_by("-id")

                return queryset
            else:
                return None
        except:
            return None


class UserProfileUASListAPIView(generics.ListAPIView):
    serializer_class = UserProfileUASListSerializer

    def get_queryset(self):
        """
        This view should return a list of all the uas
        for the currently authenticated user.
        """

        try:
            url_pk = self.kwargs.get("pk")
            user_from_url = User.objects.get(pk=url_pk)

            if user_from_url == self.request.user:

                queryset = Rpas.objects.filter(
                    organization=user_from_url.userprofile.organization
                ).order_by("-id")

                return queryset
            else:
                return None
        except:
            return None


class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        print(request.data, request.data)

        serializer = LoginSerializer(data=request.data)
        # print(serializer, "serializer")
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        # print(user, "user")
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        # return token.key

        return Response({"token": token.key}, status=200)


class SignUpAPIView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    serializer_class = SignupSerializer

    def post(self, request):
        print(request.data, "this is signup request.data")
        serializer = SignupSerializer(data=request.data)

        # print(serializer,"serializer")

        if serializer.is_valid():
            # try:
            # phone_number = request.data["phone_number"]
            # from accounts.models import SignUpPassword
            # import random

            # rand_password = random.randint(1000, 9999)
            # print("this is the random password")

            # SignUpPassword.objects.create(
            #     unregistered_user=phone_number, password=rand_password
            # )

            # from accounts.sms import send_sms

            # message = (
            #     f"{rand_password} use this code to confirm your MFUKO Registration"
            # )
            # print(message, "should be message ")

            # if not settings.IS_TESTING:
            #     print("pytest is not running")

            #     try:
            #         x = send_sms.SMS().send_sms_sync(phone_number, message)

            #         print(x, "should be sent sms ")
            #     except Exception as e:
            #         print(e, "error in sending confirmation message")
            # else:
            #     print("pytest running, hence we are not running sms client")

            # except:
            #     print("cannot create confirmation password")
            #     return Response(
            #         {
            #             "Response_Code": 1,
            #             "ResultDesc": "Cannot create confirmation password",
            #         },
            #         status=200,
            #     )

            username = request.data["username"]
            print(username, "this should be the create username")

            # first_name = request.data["first_name"]
            # print(first_name, "this should be the create first_name")

            email = request.data["email"]
            print(email, "this should be the create email")

            password = request.data["password"]
            print(password, "this should be the create password")

            try:
                user_obj = User(username=username, email=email)
                user_obj.set_password(password)

                print(user_obj, "this should be the create user_obj")

                user_obj.save()

                new_user = User.objects.get(username=username, email=email)
                django_login(request, new_user)
                token, created = Token.objects.get_or_create(user=new_user)
                # return token.key

                # return Response({"token": token.key}, status=200)
                return Response(
                    {
                        "Response_Code": 0,
                        "ResultDesc": "Initial registration successful",
                        "token": token.key,
                    },
                    status=200,
                )

            except:
                print("cannot create user")
                return Response(
                    {"Response_Code": 2, "ResultDesc": "Cannot create user"}, status=200
                )

        else:
            print("error in signup")
            return Response(data=serializer.errors, status=200)

