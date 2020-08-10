"""Users urls."""

#Django
from django.urls import include, path
from django.contrib import admin

#Django REST framework
from rest_framework import routers

#Views
from apps.users.views import UsersViewSet


router = routers.DefaultRouter()
router.register('users', UsersViewSet)


urlpatterns = [
    path('users/', include(router.urls), name='users'),
]
