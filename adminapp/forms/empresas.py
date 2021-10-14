# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from adminapp.models import Empresa


class ConfiguracionAgregarEmpresa(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    rfc = forms.CharField(min_length=12, max_length=13, required=False, label='RFC *')
    razon_social = forms.CharField(required=False,)
    nombre_comercial = forms.CharField(required=True,)
    correo_electronico = forms.EmailField(required=True,)
    logo = forms.ImageField(required=False,)

    class Meta:
        model = Empresa
        fields = [
            'rfc',
            'razon_social',
            'nombre_comercial',
            'correo_electronico',
            'logo',
        ]
        labels = {
            'correo_electronico': 'Correo Electronico *'
        }
