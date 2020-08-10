"""Users views."""

#Django REST framework
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

#Models
from django.contrib.auth.models import User

#Serializers
from apps.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """User viewset"""

    authentication_classes = [SessionAuthentication]
    permissions_classes = [permissions.IsAuthenticated,]
    queryset = User.objects.all()
    serializer_class = UserSerializer
