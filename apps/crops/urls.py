"""Crops urls."""

#Django
from django.urls import include, path

#Django REST framework
from rest_framework import routers

#Views
from apps.crops.views import CultivoViewSet, ZonaViewSet, ZonaMunicipioViewSet, TipoProductoViewSet


router = routers.DefaultRouter()
router.register(r'cul', CultivoViewSet, basename='cultivo')
router.register(r'cul', ZonaViewSet, basename='zona')
router.register(r'cul', ZonaMunicipioViewSet, basename='municipio')
router.register(r'cul', TipoProductoViewSet, basename='tipo_producto')


urlpatterns = [
    path('', include(router.urls))
]
