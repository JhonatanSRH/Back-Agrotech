"""Crops models."""

#Django
from django.db import models

#Utils
from utils.firebase import fields
from utils.firebase.functions import FunctionsFirebase


class Cultivo(models.Model):
    """Cultivo models."""

    id_cultivo = models.AutoField(primary_key=True)
    nombre_cultivo = models.CharField(max_length=50)

class TipoProducto(models.Model):
    """TipoProducto models."""

    id_tipo = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

class Zona(models.Model):
    """Zona models."""

    id_zona = models.AutoField(primary_key=True)
    codigo_departamento = models.CharField(max_length=2)
    nombre_departamento = models.CharField(max_length=50)

class ZonaMunicipio(models.Model):
    """ZonaMunicipio models."""

    id_municipio = models.AutoField(primary_key=True)
    codigo_municipio = models.CharField(max_length=5)
    id_zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    nombre_municipio = models.CharField(max_length=50)
