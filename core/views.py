from typing import Any

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

from core.models import User
from core.serializers import CreateUserSerializer, ProfileSerializer, LoginSerializer, UpdatePasswordSerializer


class SignUpView(GenericAPIView):
    """This view serves to register a new user"""

    serializer_class = CreateUserSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**serializer.data)

        return Response(ProfileSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    """This view serves to realize a login process for an existing user"""

    serializer_class = LoginSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if not user:
            raise AuthenticationFailed

        login(request=request, user=user)

        return Response(ProfileSerializer(user).data)


class ProfileView(RetrieveUpdateDestroyAPIView):
    """This view serves to get and update user data and logout from session"""

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self) -> Request:
        return self.request.user

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(GenericAPIView):
    """This view allows to update user's password"""

    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            raise AuthenticationFailed('Current password is incorrect')

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])

        return Response(serializer.data)
