# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class DatosDeControlMixin(models.Model):
    """
    Datos de control heredables para los modelos
    """

    class Meta:
        abstract = True

    eliminado = models.BooleanField(default=False,
                                    help_text='Parametro que nos dira si el objeto a sido eleminado o no')
    modificable = models.BooleanField(default=True,
                                      help_text='Parametro que nos dira si el registro puede ser modificado o no')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, help_text='Fecha en el que el registro fue creado')
    fecha_de_modificacion = models.DateTimeField(auto_now=True, help_text='Fecha en el que el registro fue modifcado',
                                                 null=True, blank=True)
    # Campos de control interno
    usuario_creo = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                     related_name='%(class)s_con_relacion_a_usuariocreo',
                                     help_text='Fk a usuario para conocer el usuario que creo el registro')
    usuario_modifico = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                         related_name='%(class)s_con_relacion_a_usuariomodifico',
                                         help_text='Fk a usuario para conocer el usuario que modifico el registro')
    usuario_elimino = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                        related_name='%(class)s_con_relacion_a_usuarioelimino',
                                        help_text='Fk a usuario para conocer el usuario que elimino el registro')
