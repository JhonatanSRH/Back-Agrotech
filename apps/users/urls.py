"""Users urls."""

#Django
from django.urls import include, path

#Django REST framework
from rest_framework import routers

#Views
from apps.users.views import UserLoginView, UserSignUpView, ProfileView


#router = routers.DefaultRouter()
#router.register(r'users', UserLoginView, basename='users')

urlpatterns = [
    path('user/login', UserLoginView.as_view()),
    path('user/signup', UserSignUpView.as_view()),
    path('user/profile', ProfileView.as_view()),
]
