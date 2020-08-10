"""Users urls."""

#Django
from django.urls import include, path
from django.contrib import admin

#Django REST framework
from rest_framework import routers

#Views
from apps.users.views import UserViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls), name="user"),
]
