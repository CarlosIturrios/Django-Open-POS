# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

import uuid
import os

from django.core.validators import RegexValidator
from django.contrib.admin import ModelAdmin
from django.db import models
from django.contrib.auth.models import User
from mainapp.models import DatosDeControlMixin


def upload_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return 'administracion/{}/logo/{}{}'.format(
        instance.rfc,
        uuid.uuid4(),
        ext
    )


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
    cer = models.FileField(upload_to='administracion/efirma', null=True, blank=True)
    key = models.FileField(upload_to='administracion/efirma', null=True, blank=True)
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

    usuarios = models.ManyToManyField(User)

    @property
    def vigente(self):
        return self.cuenta.vencimiento >= date.today()

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.rfc = self.rfc.upper()
        self.correo_electronico = self.correo_electronico.lower()
        super(Empresa, self).save(*args, **kwargs)


class EmpresaAdmin(ModelAdmin):
    search_fields = ['rfc', 'razon_social']
