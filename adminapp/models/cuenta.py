# -*- coding: utf-8 -*-
from datetime import timedelta
from datetime import date

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.admin import ModelAdmin
from django.db import models
from django.contrib.auth.models import User
from mainapp.models import DatosDeControlMixin


class Cuenta(DatosDeControlMixin):
    usuario = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='relacion_cuenta_de_usuario', default=None,
                                   help_text='Fk a usuario para conocer el usuario que propietario de la cuenta')

    cantidad_empresas = models.PositiveIntegerField(default=5, null=False)

    # cuenta
    vencimiento = models.DateField(null=True)
    cantidad_movimientos = models.PositiveIntegerField(default=500, null=True)

    # factura
    timbres_restantes = models.PositiveIntegerField(default=0, null=False)
    timbres_usados = models.PositiveIntegerField(default=0, null=False)

    # administracion
    invitado_por = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='invitado_por',
    )

    @property
    def vigente(self):
        return self.vencimiento >= date.today()

    def __str__(self):
        return str(self.usuario.username)


class CuentaAdmin(ModelAdmin):
    search_fields = ['user__username', 'usuario__email']


# Funcion para crear la cuenta despues de crear un usuario
def crear_cuenta(sender, instance, created, **kwargs):
    if not created:
        return
    cuenta = Cuenta()
    cuenta.usuario = instance
    cuenta.vencimiento = date.today() + timedelta(days=30)
    cuenta.timbres_restantes = 5
    cuenta.timbres_usados = 0
    cuenta.save()


# Conectar funcion para crear cuenta despues de crear un usuario
post_save.connect(crear_cuenta, sender=get_user_model())
