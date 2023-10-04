# -*- coding: utf-8 -*-
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.utils import timezone

from mainapp.models import Product
from adminapp.models import Empresa
from mainapp import forms
from .index import validar_horario
from .index import append_product_to_cart

@login_required()
def productos_view(request, pk):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR,
                             'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    if request.method == "POST":
        return append_product_to_cart(request, empresa, pk)
    productos = Product.objects.filter(
        category_id=pk, eliminado=False, empresa=empresa).order_by('-stock')
    return render(request, 'mvcapp/productos/productos.html',
                  {'productos': productos, 'empresa_pk': empresa.pk})


@login_required()
def listar_productos_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR,
                             'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    productos = Product.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/productos/listar_productos.html',
                  {'productos': productos, 'empresa_pk': empresa.pk})


@login_required()
def crear_nuevo_producto_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR,
                             'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')
    if request.method == 'POST':

        form = forms.form_agregar_product(request.POST, request.FILES, empresa=empresa)

        if form.is_valid():
            with transaction.atomic():
                product_code = form.cleaned_data['product_code']
                if Product.objects.filter(product_code=product_code, empresa=empresa).exists():
                    form.add_error(
                        'product_code', 'El código de producto ya existe')
                    return render(request, 'mvcapp/productos/modificar_producto.html', {'form': form})

                producto = form.save(commit=False)
                producto.empresa = empresa
                producto.save()
                producto.ingredients.set(form.cleaned_data['ingredients'])

                messages.add_message(request, messages.INFO,
                                     'Producto agregado con éxito')
                return redirect('mainapp:listar_productos_view')
        else:
            return render(request, 'mvcapp/productos/crear_producto.html',
                          {'form': form, 'empresa_pk': empresa.pk})

    else:
        form = forms.form_agregar_product(empresa=empresa)

    return render(request, 'mvcapp/productos/crear_producto.html',
                  {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def modificar_producto_view(request, pk=None):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR,
                             'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    if request.method == 'POST':
        form = forms.form_agregar_product(request.POST, request.FILES, empresa=empresa)
        if form.is_valid():
            if pk:
                product = get_object_or_404(Product, pk=pk, empresa=empresa)
                # Verificar si se proporcionó una nueva imagen en el formulario
                if 'image' in form.changed_data:
                    product.image = form.cleaned_data['image']
                product.name = form.cleaned_data['name']
                product.description = form.cleaned_data['description']
                # Actualizar los demás campos
                product.category = form.cleaned_data['category']
                product.price = form.cleaned_data['price']
                product.stock = form.cleaned_data['stock']
                product.barcode = form.cleaned_data['barcode']
                product.currency = form.cleaned_data['currency']
                # Actualizar los ingredientes
                product.ingredients.set(form.cleaned_data['ingredients'])
                product.save()
                messages.add_message(request, messages.INFO,
                                     'Producto modificado con éxito')
                return redirect('mainapp:listar_productos_view')
            else:
                messages.add_message(
                    request, messages.WARNING, 'Método no permitido')
                return redirect('mainapp:listar_productos_view')
        else:
            return render(request, 'mvcapp/productos/modificar_producto.html', {'form': form, 'empresa_pk': empresa.pk})
    else:
        if pk:
            product = get_object_or_404(Product, pk=pk, empresa=empresa)
            form = forms.form_agregar_product(
                instance=product, empresa=empresa ,initial={'image': product.image})
        else:
            form = forms.form_agregar_product(empresa=empresa)

    return render(request, 'mvcapp/productos/modificar_producto.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def eliminar_producto_view(request, pk=None):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR,
                             'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    product = get_object_or_404(Product, pk=pk, empresa=empresa)

    if request.method == 'POST':
        product.delete()
        messages.add_message(request, messages.INFO,
                             'El Producto se ha eliminado con éxito')
        return redirect('mainapp:listar_productos_view')

    else:
        messages.add_message(request, messages.WARNING, 'Metodo no permitido')
        return redirect('mainapp:listar_productos_view')


# sin auth para customer
def productos_customer_view(request, cadena, pk):
    empresa = get_object_or_404(Empresa, nombre_para_pagos=cadena)
    if empresa.horario_de_acceso:
        hora_actual = timezone.localtime(timezone.now()).time()
        hora_inicio = empresa.horario_de_acceso.hora_inicio
        hora_fin = empresa.horario_de_acceso.hora_fin
        if not validar_horario(hora_inicio, hora_fin, hora_actual):    
            messages.add_message(request, messages.WARNING, 'La empresa está fuera de horario')
            return redirect('website:website')
    if not empresa.vigente:
        messages.add_message(request, messages.WARNING,
                             'La empresa presenta adeudo y no tiene disponible la sección de pedidos')
        return redirect('administracion:registro')

    if request.method == "POST":
        append_product_to_cart(request, empresa, pk)

    productos = Product.objects.filter(
        category_id=pk, eliminado=False, empresa=empresa).order_by('-stock')

    return render(request, 'mvcapp/productos/productos_costumers.html',
                  {'productos': productos, 'cadena': cadena, 'empresa_pk': empresa.pk, 'empresa': empresa})

