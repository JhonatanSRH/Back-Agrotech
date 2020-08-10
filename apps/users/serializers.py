"""Users serialiezers."""

#Django
from django.contrib.auth.models import User

#Django REST framework
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        model = User
        fields = '__all__'
