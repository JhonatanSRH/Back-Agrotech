"""agrotech urls."""

#Django
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]
