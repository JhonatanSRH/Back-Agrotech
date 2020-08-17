"""Posts models."""

#Django
from django.db import models

#Utils
from utils.firebase import fields
from utils.firebase.functions import FunctionsFirebase


class UserPost(FunctionsFirebase):
    """UserPost firebase."""

    ruta_raiz = "posts"
    id_usuario = fields.IntegerField()
    username = fields.CharField()
    fecha_post = fields.DatetimeField(auto_now=True)
    likes = fields.IntegerField(default=0)
    comentarios = fields.IntegerField(default=0)
    abierto = fields.BooleanField(default=True)
    titulo = fields.CharField(max_length=30)
    id_cultivo = fields.IntegerField(default=0)
    nombre_cultivo = fields.CharField(max_length=20, default="Ninguno")

class PostCultivo(FunctionsFirebase):
    """PostCultivo firebase."""

    ruta_raiz = "posts/{0}/cultivo"
    nombre_cultivo = fields.CharField(max_length=20)
    descripcion_cultivo = fields.CharField(max_length=200)
    url_imagen = fields.CharField(max_length=50)
    numero_temperatura = fields.FloatField(decimal_places=6)
    id_municipio = fields.IntegerField()
    nombre_departamento = fields.CharField(max_length=50)
    nombre_municipio = fields.CharField(max_length=50)
    edad_cosecha = fields.FloatField(decimal_places=2)
    densidad_cultivo = fields.FloatField(decimal_places=6)

class ActividadesCultivo(FunctionsFirebase):
    """AcctionesCultivo firebase."""

    ruta_raiz = "posts/{0}/acciones"
    nombre_accion = fields.CharField(max_length=50)
    descripcion = fields.CharField(max_length=200)

class ProductoCultivo(FunctionsFirebase):
    """ProductoCultivo firebase."""

    ruta_raiz = "posts/{0}/productos"
    nombre_producto = fields.CharField(max_length=50)
    descripcion = fields.CharField(max_length=200)
