import os
from django.db import models

from mainapp.models import DatosDeControlMixin


class Customer(DatosDeControlMixin):
    name = models.CharField(max_length=240, null=False, blank=False, help_text='Customer name')
    cellphone = models.CharField(max_length=20, null=False, blank=False, help_text='Customer cellphone', unique=True)
    direction = models.TextField(null=True, blank=True, help_text='Customer direction')
    pay_method = models.CharField(max_length=120, null=True, blank=True, help_text='Customer pay_method')
    observations = models.TextField(null=True, blank=True, help_text='Customer observations')
    email = models.EmailField(blank=True, null=True, help_text='Customer email field, to save the contact email',
                              unique=False)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.pk, self.name, self.email)
