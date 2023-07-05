# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.safestring import mark_safe

from adminapp.models import Empresa


class ConfiguracionAgregarEmpresa(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    rfc = forms.CharField(min_length=12, max_length=13,
                          required=False, label='RFC *')
    razon_social = forms.CharField(required=False,)
    nombre_comercial = forms.CharField(required=True,)
    correo_electronico = forms.EmailField(required=True,)
    logo = forms.ImageField(required=False,)
    nombre_para_pagos = forms.CharField(required=True,)

    class Meta:
        model = Empresa
        fields = [
            'rfc',
            'razon_social',
            'nombre_comercial',
            'correo_electronico',
            'logo',
            'nombre_para_pagos',
        ]
        labels = {
            'correo_electronico': 'Correo Electronico *'
        }


class EmpresaForm(forms.ModelForm):
    nombre_para_pagos = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    cuenta = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = Empresa
        fields = [
            'razon_social',
            'nombre_comercial',
            'rfc',
            'correo_electronico',
            'logo',
            'nombre_para_pagos',
            'sdk_private',
            'sdk_public',
            'ciudades_permitidas',
            'usuarios',
            'cer',
            'key',
            'contrasena',
            ]

        widgets = {            
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XAXX010101000'}),
            'cer': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'key': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ciudades_permitidas': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'usuarios': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'sdk_private': forms.TextInput(attrs={'class': 'form-control'}),
            'sdk_public': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuarios'].queryset = self.instance.usuarios.all()
        self.fields['sdk_private'].label = mark_safe('SDK Private<a href="https://www.mercadopago.com.mx/developers/es/docs/checkout-pro/additional-content/your-integrations/credentials" target="_blank" title="Mercado Pago SDK Credentials"> - ¿Aún no tienes tus credenciales? Haz clic aquí</a>')
    
        cuenta_instance = self.instance.cuenta
        if cuenta_instance:
            cuenta_data = f"Vencimiento: {cuenta_instance.vencimiento}, Cantidad de movimientos: {cuenta_instance.cantidad_movimientos}, Timbres restantes: {cuenta_instance.timbres_restantes}, Timbres utilizados: {cuenta_instance.timbres_usados}"
            self.fields['cuenta'].widget.attrs['value'] = cuenta_data
    