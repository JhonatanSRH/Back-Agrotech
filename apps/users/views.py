"""Users views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from apps.users.permissions import IsAccountOwner

# Serializers
from apps.users.serializers import ProfileModelSerializer
from apps.users.serializers import (
    AccountVerificationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserSignUpSerializer
)

# Models
from apps.users.models import User, Profile


class UserLoginView(APIView):
    """UserLogin view."""

    def post(self, request, *args, **kwargs):
        """Iniciar sesion."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        response = {
                    "user": UserSerializer(user).data,
                    "token": token
        }
        return Response(response, status=status.HTTP_201_CREATED)

class UserSignUpView(APIView):
    """UserSignUp view."""

    def post(self, request, *args, **kwargs):
        """Iniciar sesion."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = UserSerializer(user).data
        return Response(response, status=status.HTTP_201_CREATED)

class ProfileView(APIView):
    """Profile view."""

    def put(self, request, *args, **kwargs):
        """Actualizar perfil."""
        try:
            user = User.objects.filter(username=request.query_params['username'])
            if user.count() <= 0:
                return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            profile = user[0].profile
            serializer = ProfileModelSerializer(
                profile,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = UserSerializer(user[0]).data
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"Error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
