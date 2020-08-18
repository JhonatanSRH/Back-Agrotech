"""Posts views."""

#Utils
import copy
import os
import sys
import logging as log

#Django REST framework
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response

#Models
from apps.posts.models import PostCultivo, UserPost, ActividadesCultivo, ProductoCultivo
from utils.image_manager import upload_blob


class PostCultivoView(APIView):
    """PostCultivoView"""

    __request = {}
    __response = {}
    data = []
    __modelo_actividades = ActividadesCultivo()
    __modelo_productos = ProductoCultivo()

    def post(self, request):
        self.__request = request.data
        model_fb_upost = UserPost(pk=self.__request['id_post'])
        model_fb_upost.__tablename__ = model_fb_upost.ruta_raiz
        if len(model_fb_upost.get()) <= 0:
            return Response({"message": "Post no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        model_fb = PostCultivo(pk=self.__request['id_cultivo'], data=self.__request)
        model_fb.__tablename__ = model_fb.ruta_raiz.format(self.__request['id_post'])
        self.data = model_fb.get()
        if not None in self.data:
            return Response({"message": "Ya tiene un post del cultivo que intenta ingresar."}, status=status.HTTP_409_CONFLICT)
        model_error = model_fb.valide()
        if len(model_error) > 0:
            return Response({"message": "Datos erroneos."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.validar_detalles_cultivo(self.__modelo_actividades, self.__request['actividades'], self.__request['id_post'])
            self.validar_detalles_cultivo(self.__modelo_productos, self.__request['productos'], self.__request['id_post'])
        except Exception as error:
            return Response({"message": "Datos erroneos.", "description": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        model_fb.save()
        self.guardar_multiple_data(self.__modelo_actividades, self.__request['actividades'])
        self.guardar_multiple_data(self.__modelo_productos, self.__request['productos'])
        model_fb_upost.data = {
                               "id_cultivo": self.__request['id_cultivo'],
                               "nombre_cultivo": self.__request['nombre_cultivo'],
                               "abierto": False
                               }
        model_fb_upost.save(update=True)
        return Response({"message": "Creado."}, status=status.HTTP_201_CREATED)

    def get(self, request):
        self.__request = request.query_params
        model_fb_upost = UserPost(pk=self.__request['post'])
        model_fb_upost.__tablename__ = model_fb_upost.ruta_raiz
        self.data = model_fb_upost.get()
        if None in self.data:
            return Response({"message": "Post no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        self.__response['dato_post'] = self.data[0].copy()
        id_post = self.data[0]['id']
        self.rellenar_detalle_post(PostCultivo, 'dato_cultivo', id_post)
        self.rellenar_detalle_post(ActividadesCultivo, 'dato_actividad', id_post)
        self.rellenar_detalle_post(ProductoCultivo, 'dato_producto', id_post)
        return Response(self.__response, status=status.HTTP_200_OK)

    def rellenar_detalle_post(self, model, respose_key, *path_format):
        """Completa la respuesta con diccionarios para los modelos que lleguen."""
        model.__tablename__ = model.ruta_raiz.format(*path_format)
        self.data = model.get()
        if None in self.data or len(self.data) <= 0:
            self.__response[respose_key] = {}
        else:
            self.__response[respose_key] = self.data.copy()

    def validar_detalles_cultivo(self, model, data, *path_format):
        """Valida que el modelo tenga la informacion necesaria para ser guardado"""
        model.__tablename__ = model.ruta_raiz.format(*path_format)
        for dict_data in data:
            model.data = dict_data
            model_error = model.valide()
            if len(model_error) > 0:
                raise Exception(model_error)

    def guardar_multiple_data(self, model, list_data):
        for index, dato in enumerate(list_data):
            print(dato)
            model.id.value = index + 1
            model.data = dato
            model.valide()
            model.save()

class PostView(APIView):
    """PostCultivoView view.
    Crea la fase inicial de un post."""

    __request = {}
    __filtros = []
    data = []

    def post(self, request):
        self.__request = request.data
        model_fb_upost = UserPost(data=self.__request)
        model_fb_upost.__tablename__ = model_fb_upost.ruta_raiz
        self.data = model_fb_upost.get()
        if not None in self.data:
            posts_activos = [dict_data['abierto'] for dict_data in self.data]
            if True in posts_activos:
                return Response({"message": "Ya tiene un post abierto, por favor complételo."}, status=status.HTTP_409_CONFLICT)
        model_error = model_fb_upost.valide()
        if len(model_error) > 0:
            return Response({"message": "Datos erroneos."}, status=status.HTTP_400_BAD_REQUEST)
        model_fb_upost.save()
        return Response(model_fb_upost.get(), status=status.HTTP_201_CREATED)

    def get(self, request):
        try:
            self.__request = request.query_params
            model_fb_upost = UserPost()
            model_fb_upost.__tablename__ = model_fb_upost.ruta_raiz
            self.__filtros.clear()
            if 'cultivo' in self.__request:
                self.__filtros += [('id_cultivo', '==', int(self.__request['cultivo']))]
            if len(self.__filtros) > 0:
                self.data = model_fb_upost.get(filters=self.__filtros)
            else:
                self.data = model_fb_upost.get()
            if 'username' in self.__request:
                data_aux = []
                for dict_dato in self.data:
                    if dict_dato['username'].lower() == self.__request['username'].lower():
                        data_aux.append(dict_dato)
                self.data = data_aux
            if None in self.data:
                return Response({"message": "Aún no se ha registrado ningun post."}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.data, status=status.HTTP_200_OK)
        except KeyError as error:
            return Response({"message": "Datos erroneos." + str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            self.__request = request.query_params
            model_fb_upost = UserPost(pk=self.__request['post'])
            model_fb_upost.__tablename__ = model_fb_upost.ruta_raiz
            if None in (model_fb_upost.get()):
                return Response({"message": "Post no encontrado."} ,status=status.HTTP_404_NOT_FOUND)
            self.eliminar_subcoleccion(PostCultivo)
            self.eliminar_subcoleccion(ActividadesCultivo)
            self.eliminar_subcoleccion(ProductoCultivo)
            model_fb_upost.delete()
            return Response({"message": "Eliminado."} ,status=status.HTTP_204_NO_CONTENT)
        except KeyError as error:
            return Response({"message": "Datos erroneos." + str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def eliminar_subcoleccion(self, model):
        model.__tablename__ =  model.ruta_raiz.format(self.__request['post'])
        model.delete_all_documents()

class ImageManagerView(APIView):

    parser_classes = [FileUploadParser]

    def post(self, request):
        try:
            upload_blob(request.data['image'],request.data['name'])
            return Response(status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"message": str(error)} ,status=status.HTTP_201_CREATED)

    def put(self, request, filename, format=None):
        try:
            file_obj = request.FILES
            print(file_obj)
            return Response(status=204)
        except Exception as error:
            return Response({"message": str(error)} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
