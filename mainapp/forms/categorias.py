# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from mainapp.models import Category, Currency, QuantityType, Ingredient, Place, Product, Customer


class form_agregar_categoria(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    description = forms.CharField(required=True, )
    image = forms.ImageField(required=True, )

    class Meta:
        model = Category
        exclude = ('empresa',)
        fields = [
            'description',
            'image',
        ]


class form_agregar_currency(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    description = forms.CharField(required=False, )
    symbol = forms.CharField(required=False, )

    class Meta:
        model = Currency
        exclude = ('empresa',)
        fields = [
            'description',
            'symbol',
        ]


class form_agregar_quantity_type(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    description = forms.CharField(required=False, )

    class Meta:
        model = QuantityType
        exclude = ('empresa',)
        fields = [
            'description',
        ]


class form_agregar_ingredient(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    name = forms.CharField(required=False, )
    description = forms.Textarea()
    clasification = forms.CharField(required=False, )
    quantity = forms.CharField(required=False, )
    quantity_type = forms.ModelChoiceField(queryset=QuantityType.objects.filter(eliminado=False))

    class Meta:
        model = Ingredient
        exclude = ('empresa',)
        fields = [
            'name',
            'description',
            'clasification',
            'quantity',
            'quantity_type',
        ]


class form_agregar_place(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    description = forms.CharField(required=False, )
    direction = forms.Textarea()

    class Meta:
        model = Place
        exclude = ('empresa',)
        fields = [
            'description',
            'direction',
        ]


class form_agregar_product(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    name = forms.CharField(required=True, )
    description = forms.Textarea()
    category = forms.ModelChoiceField(queryset=Category.objects.filter(eliminado=False))
    image = forms.ImageField(required=True, )
    price = forms.FloatField(required=True, )
    stock = forms.IntegerField(required=True, )
    barcode = forms.CharField(required=True, )
    product_code = forms.CharField(required=True, )
    currency = forms.ModelChoiceField(queryset=Currency.objects.filter(eliminado=False))

    class Meta:
        model = Product
        exclude = ('empresa', 'ingredients')
        fields = [
            'name',
            'description',
            'category',
            'image',
            'price',
            'stock',
            'product_code',
            'barcode',
            'currency',
        ]


class form_agregar_customer(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    name = forms.CharField(required=False, )
    cellphone = forms.CharField(required=True, min_length=10, max_length=13)
    direction = forms.Textarea()
    pay_method = forms.CharField(required=False, )
    observations = forms.Textarea()
    email = forms.EmailField(required=False, )

    class Meta:
        model = Customer
        exclude = ('empresa',)
        fields = [
            'name',
            'cellphone',
            'direction',
            'pay_method',
            'observations',
            'email',
        ]
