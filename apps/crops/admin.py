"""Crops admin."""

from django.contrib import admin
from apps.crops.models import Cultivo
from apps.crops.models import Zona
from apps.crops.models import ZonaMunicipio
from apps.crops.models import TipoProducto

admin.site.register(Cultivo)
admin.site.register(Zona)
admin.site.register(ZonaMunicipio)
admin.site.register(TipoProducto)
