# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

import uuid
import os

from django.utils.text import slugify
from django.core.validators import RegexValidator
from django.contrib.admin import ModelAdmin
from django.db import models
from django.contrib.auth.models import User
from mainapp.models import DatosDeControlMixin


def eliminar_espacios_blancos(valor):
    return valor.strip().replace(" ", "")


def upload_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return 'administracion/{}/logo/{}{}'.format(
        instance.rfc,
        uuid.uuid4(),
        ext
    )

class CiudadadPermitida(DatosDeControlMixin):
    description = models.CharField(
        max_length=100, null=False, blank=False, help_text='Ciudada permitida Description'
    )

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.description)


class CiudadadPermitidaAdmin(ModelAdmin):
    search_fields = ['description'] 

class HorarioAcceso(DatosDeControlMixin):    
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        hora_inicio_str = self.hora_inicio.strftime("%I:%M %p")
        hora_fin_str = self.hora_fin.strftime("%I:%M %p")
        return f"{self.pk} - Hora de inicio: {hora_inicio_str} - Hora de cierre: {hora_fin_str}"
    
class HorarioAccesoAdmin(ModelAdmin):
    search_fields = ['hora_inicio'] 

class Empresa(DatosDeControlMixin):
    rfc = models.CharField(
        max_length=13, blank=True, null=True, unique=True,
        validators=[
            RegexValidator(
                regex='^([A-Z&Ññ]{3,4}|[A-Z][AEIOU][A-Z]{2})\d{2}((01|03|05|07|08|10|12)(0[1-9]|[12]\d|3[01])|02(0[1-9]|[12]\d)|(04|06|09|11)(0[1-9]|[12]\d|30))([A-Z0-9]{2}[0-9A])?$',
                message='El formato del RFC no es correcto. Ej. XAXX010101000'
            )
        ]
    )
    razon_social = models.CharField(
        max_length=250, blank=False, null=False, db_index=True, verbose_name='Razón social *'
    )
    nombre_comercial = models.CharField(
        max_length=200, blank=False, null=False, db_index=True, verbose_name='Nombre comercial *'
    )
    # Facturacion
    cer = models.FileField(
        upload_to='administracion/efirma', null=True, blank=True)
    key = models.FileField(
        upload_to='administracion/efirma', null=True, blank=True)
    contrasena = models.CharField(max_length=20, null=True, blank=True)
    correo_electronico = models.EmailField(blank=False, null=False)
    logo = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True,
        help_text='Su imagen se re-dimensionara (200px~100px)',
    )

    cuenta = models.ForeignKey('adminapp.Cuenta', on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='relacion_cuenta_a_empresa',
                               help_text='Fk a cuenta de usuario a la que pertenece la empresa')

    ciudades_permitidas = models.ManyToManyField(
        CiudadadPermitida,
        blank=True,
        related_name='relacion_ciudades_permitidas_a_empresa',
        help_text='Ciudades permitidas a las que pertenece la empresa'
    )
    usuarios = models.ManyToManyField(User)
    sdk_private = models.CharField(max_length=100, unique=True, null=True, blank=True, default=None)
    sdk_public = models.CharField(max_length=100, unique=True, null=True, blank=True, default=None)
    horario_de_acceso = models.ForeignKey(HorarioAcceso, null=True, blank=True, default=None, on_delete=models.CASCADE,
                                       related_name='horarios_acceso', help_text="Horario de acceso al portal del cliente.")

    nombre_para_pagos = models.CharField(
        max_length=200, blank=False, null=True, db_index=True, verbose_name='Nombre con el que accederán los clientes de esta empresa*'
    )

    @property
    def vigente(self):
        return self.cuenta.vencimiento >= date.today()

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.rfc = self.rfc.upper()
        self.correo_electronico = self.correo_electronico.lower()
        self.nombre_para_pagos = eliminar_espacios_blancos(
            self.nombre_para_pagos)
        super(Empresa, self).save(*args, **kwargs)


class EmpresaAdmin(ModelAdmin):
    search_fields = ['rfc', 'razon_social']


class PaymentWithMercadoPago(DatosDeControlMixin):
    action = models.CharField(max_length=255,null=True, blank=True)
    api_version = models.CharField(max_length=10,null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    data_id = models.BigIntegerField(unique=True,null=True, blank=True)
    live_mode = models.BooleanField(default=False, null=True, blank=True)
    payment_type = models.CharField(max_length=255, null=True, blank=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, help_text='Es lo mismo que collector_id y preference_id' , null=False, blank=False)
    coupon_code = models.CharField(max_length=255, null=True, blank=True)
    coupon_labels = models.CharField(max_length=255, null=True, blank=True)
    date_of_expiration = models.DateTimeField(null=True, blank=True)
    expiration_date_from = models.DateTimeField(null=True, blank=True)
    expiration_date_to = models.DateTimeField(null=True, blank=True)
    expires = models.BooleanField(default=False, null=True, blank=True)
    external_reference = models.CharField(max_length=255, null=True, blank=True)
    init_point = models.URLField(max_length=200, null=True, blank=True)
    internal_metadata = models.JSONField(null=True, blank=True)
    items = models.JSONField(null=True, blank=True)
    nueva_orden = models.JSONField(null=True, blank=True)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment ID: {self.payment_id}, User ID:"

class PaymentWithMercadoPagoAdmin(ModelAdmin):
    search_fields = ['user_id', 'coupon_code', 'external_reference', 'data_id']
