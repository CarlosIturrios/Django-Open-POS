from django.db import models

from mainapp.models import DatosDeControlMixin


class Currency(DatosDeControlMixin):
    """
    La tabla contiene la información de las categorías de solicitudes registradas en el sistema.
    """
    description = models.CharField(max_length=100, null=False, blank=False, help_text='Currency type Description')
    symbol = models.CharField(max_length=100, null=False, blank=False, help_text='Currency symbol')

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.description)

