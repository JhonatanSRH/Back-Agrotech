"""Crops serializer."""

#Django REST framework
from rest_framework import serializers

#Models
from apps.crops.models import Cultivo, Zona, ZonaMunicipio, TipoProducto


class CultivoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Cultivo
        fields = '__all__'

class ZonaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Zona
        fields = '__all__'

class ZonaMunicipioSerializer(serializers.ModelSerializer):

    class Meta:

        model = ZonaMunicipio
        fields = '__all__'

class TipoProductoSerializer(serializers.ModelSerializer):

    class Meta:

        model = TipoProducto
        fields = '__all__'
