# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unicodedata
from django.core.validators import MinValueValidator

from django import forms

from mainapp.models import Category, Currency, QuantityType, Ingredient, Place, Product, Customer


class form_agregar_categoria(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    clave = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'H01'})
    )
    description = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Hamburguesas'})
    )
    image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Category
        exclude = ('empresa',)
        fields = [
            'description',
            'clave',
            'image',
        ]

    def clean_description(self):
        description = self.cleaned_data['description']

        # Normalize and encode the description to remove non-ASCII characters
        sanitized_description = unicodedata.normalize('NFKD', description).encode('ascii', 'ignore').decode('ascii')

        return sanitized_description


class form_modificar_categoria(forms.ModelForm):
    clave = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'H01'})
    )
    description = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Hamburguesas'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Category
        exclude = ('empresa',)

        fields = [
            'description',
            'clave',
            'image',
        ]

    def __init__(self, *args, **kwargs):
        categoria_instance = kwargs.get('instance')
        if categoria_instance:
            kwargs['initial'] = {
                'categoria_id': categoria_instance.id,
            }
        super().__init__(*args, **kwargs)
        self.fields['categoria_id'] = forms.CharField(widget=forms.HiddenInput)
        self.fields['categoria_id'].label = ''


class form_agregar_currency(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    description = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'MXN'}))
    symbol = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '$'}))

    class Meta:
        model = Currency
        exclude = ('empresa',)
        fields = [
            'description',
            'symbol',
        ]
        labels = {
            'description': 'Descripción de la moneda',
            'symbol': 'Símbolo',
        }


class form_agregar_quantity_type(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    description = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'MXN'}))

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
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Tomate'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Tomate rojo del sur'}))
    clasification = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Verduras'}))
    quantity = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    quantity_type = forms.ModelChoiceField(
        queryset=QuantityType.objects.filter(eliminado=False),
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )

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

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)  # Obtén y elimina 'empresa' de kwargs
        super(form_agregar_ingredient, self).__init__(*args, **kwargs)
        self.fields['quantity_type'].queryset = QuantityType.objects.filter(empresa=empresa)


class form_agregar_place(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    description = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Matriz'}))

    direction = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'AV. de las principales entre calles de las secundarias #connumero'}))

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
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ej. Hamburguesa, Refresco de limon'}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Ej. Hamburguesa con queso bañada en bbq'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(eliminado=False),
        widget=forms.Select(attrs={'class': 'form-control custom-select'}))
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    price = forms.DecimalField(required=True, validators=[MinValueValidator(0.0)],
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    stock = forms.IntegerField(required=True, validators=[MinValueValidator(0)],
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    barcode = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ej. 11222'}))
    product_code = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'EJ. HA212'}))
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(eliminado=False),
        widget=forms.Select(attrs={'class': 'form-control custom-select'}))
    ingredients = forms.ModelMultipleChoiceField(required=False,
                                                 queryset=Ingredient.objects.filter(
                                                     eliminado=False),
                                                 widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    def clean_description(self):
        description = self.cleaned_data['description']
        # Normalizar y codificar la descripción para evitar problemas de codificación
        return unicodedata.normalize('NFKD', description).encode('ascii', 'ignore').decode('utf-8')
    
    class Meta:
        model = Product
        exclude = ('empresa',)
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
            'ingredients',
        ]

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)  # Obtén y elimina 'empresa' de kwargs
        super(form_agregar_product, self).__init__(*args, **kwargs)
        self.fields['currency'].queryset = Currency.objects.filter(empresa=empresa)
        self.fields['category'].queryset = Category.objects.filter(empresa=empresa)
        self.fields['ingredients'].queryset = Ingredient.objects.filter(empresa=empresa)

class form_customer(forms.ModelForm):
    """ ConfiguracionAgregarEmpresa
    Formulario para agregar empresa dentro de administracion
    """
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    cellphone = forms.CharField(required=True, min_length=10, max_length=13,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    direction = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    pay_method = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    observations = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

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
