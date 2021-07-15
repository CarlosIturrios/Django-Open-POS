import os
from django.db import models

from mainapp.models import DatosDeControlMixin


class Customer(DatosDeControlMixin):
    name = models.CharField(max_length=240, null=False, blank=False, help_text='Customer name')
    cellphone = models.CharField(max_length=20, null=False, blank=False, help_text='Product name')
    direction = models.TextField(null=False, blank=False, help_text='Product name')
    pay_method = models.CharField(max_length=120, null=False, blank=False, help_text='Product name')
    observations = models.TextField(null=False, blank=False, help_text='Product name')
