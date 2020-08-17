"""Users urls."""

#Django
from django.urls import include, path

#Django REST framework
from rest_framework import routers

#Views
from apps.users.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
