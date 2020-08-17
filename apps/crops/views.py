"""Crops views."""


#Django REST framework
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

#Models
from apps.crops.models import Cultivo, Zona, ZonaMunicipio, TipoProducto

#Serializers
from apps.crops.serializers import CultivoSerializer, ZonaSerializer, ZonaMunicipioSerializer, TipoProductoSerializer


class CultivoViewSet(viewsets.GenericViewSet):
    """Cultivos View.
    Lista los cultivos que se encuentren en base de datos"""

    queryset = Cultivo.objects.all()
    serializer = CultivoSerializer(queryset, many=True)

    @action(detail=False, methods=['get'])
    def cultivos(self, request):
        """Lista de cultivos."""
        return Response(self.serializer.data, status=status.HTTP_200_OK)

class ZonaViewSet(viewsets.GenericViewSet):
    """Zona View.
    Lista las zonas registradas"""

    queryset = Zona.objects.all()
    serializer = ZonaSerializer(queryset, many=True)

    @action(detail=False, methods=['get'])
    def departamentos(self, request):
        """Lista de zonas."""
        return Response(self.serializer.data, status=status.HTTP_200_OK)

class ZonaMunicipioViewSet(viewsets.GenericViewSet):
    """ZonaMunicipio View.
    Lista los municipios registrados"""

    queryset = ZonaMunicipio.objects.all()
    serializer = ZonaMunicipioSerializer(queryset, many=True)

    @action(detail=False, methods=['get'])
    def municipios(self, request):
        """Lista de municipios."""
        return Response(self.serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def municipio(self, request):
        try:
            queryset = ZonaMunicipio.objects.filter(**request.query_params)
            if queryset.count() <= 0:
                return Response({"message": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"message": "Parametros invalidos.", "description": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ZonaMunicipioSerializer(queryset, many=True)
        return Response(self.serializer.data, status=status.HTTP_200_OK)

class TipoProductoViewSet(viewsets.GenericViewSet):
    """TipoProducto View.
    Lista los tipos de producto posibles"""

    queryset = TipoProducto.objects.all()
    serializer = TipoProductoSerializer(queryset, many=True)

    @action(detail=False, methods=['get'])
    def productos(self, request):
        """Lista de tipos de producto."""
        return Response(self.serializer.data, status=status.HTTP_200_OK)
