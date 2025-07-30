from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenBlacklistSerializer,
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework import status, exceptions
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from youtube_clone.users.api.serializers import UserSerializer, UserCustomSerializer, UserMeReadSerializer
from youtube_clone.users.use_cases.create_user import CreateUserUseCase

from youtube_clone.users.models import User


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(
        detail=False,
        methods=["POST"],
        url_path="auth",
        serializer_class=TokenObtainPairSerializer,
        permission_classes=[AllowAny],
    )
    def auth(self, request, pk=None):
        serializer = TokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        except exceptions.AuthenticationFailed:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Invalid credentials"})

    @action(detail=False, methods=["post"], url_path="sign-up")
    def sign_up(self, request):
        try:
            user = CreateUserUseCase.build().execute(params=request.data)
        except IntegrityError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCustomSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["POST"],
        url_path="auth/refresh",
        serializer_class=TokenRefreshSerializer,
        permission_classes=[AllowAny],
    )
    def auth_refresh(self, request, pk=None):
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except TokenError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(
        detail=False,
        methods=["POST"],
        url_path="auth/sign-out",
        serializer_class=TokenBlacklistSerializer,
        permission_classes=[IsAuthenticated],
    )
    def auth_sign_out(self, request, pk=None):
        serializer = TokenBlacklistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserMeReadSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
