from django.db import models


class DatosDeControlMixin(models.Model):
    """
    Datos de control heredables para los modelos
    """

    class Meta:
        abstract = True

    eliminado = models.BooleanField(default=True, help_text='Parametro que nos dira si el objeto a sido eleminado o no')
    modificable = models.BooleanField(default=True,
                                      help_text='Parametro que nos dira si el registro puede ser modificado o no')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, help_text='Fecha en el que el registro fue creado')
    fecha_de_modificacion = models.DateTimeField(auto_now=True, help_text='Fecha en el que el registro fue modifcado',
                                                 null=True, blank=True)
