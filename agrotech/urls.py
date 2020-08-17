"""agrotech urls."""

#Django
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('', include('apps.crops.urls')),
    path('', include('apps.posts.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]
