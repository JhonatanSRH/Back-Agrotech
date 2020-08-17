"""Crops urls."""

#Django
from django.urls import include, path

#Views
from apps.posts.views import PostCultivoView, PostView

urlpatterns = [
    path('post/cultivo', PostCultivoView.as_view()),
    path('post/posts', PostView.as_view()),
]
