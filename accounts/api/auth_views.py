import email

from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from accounts.api.serializers import SignupSerializer, LoginSerializer

User = get_user_model()


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # Check if identifier matches username or email
            try:
                user_obj = User.objects.get(email=identifier)
                email = user_obj.email
            except User.DoesNotExist:
                return Response({"error": "Invalid email"}, status=status.HTTP_401_UNAUTHORIZED)

            user = authenticate(email=email, password=password)
            if user:
                Token.objects.get_or_create(user=user)
                token = Token.objects.get(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
