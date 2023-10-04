# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.utils import timezone

from mainapp.models import Category
from mainapp.models import Product
from adminapp.models import Empresa
from mainapp import views
from mainapp import forms
from .index import validar_horario


@login_required()
def listar_categorias_view(request):
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

    categorias = Category.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/categorias/listar_categorias.html',
                  {'categorias': categorias, 'empresa_pk': empresa.pk})


@login_required()
def categorias_view(request):
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
    categorias = Category.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/categorias/categorias.html',
                  {'categorias': categorias, 'empresa_pk': empresa.pk})


@login_required()
def crear_nueva_categoria_view(request):
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

        form = forms.form_agregar_categoria(request.POST, request.FILES)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.empresa = empresa
            categoria.save()
            messages.add_message(request, messages.INFO,
                                 'Categoria agregada con exito')
            return redirect('mainapp:listar_categorias_view')
        else:
            return render(request, 'mvcapp/categorias/crear_categoria.html', {'form': form, 'empresa_pk': empresa.pk})

    else:
        form = forms.form_agregar_categoria()
        form.fields['description'].label = 'Descripción de la categoria'
        form.fields['clave'].label = 'Clave de la categoria'
        form.fields['image'].label = 'Imagen de la categoria'

    return render(request, 'mvcapp/categorias/crear_categoria.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def modificar_categoria_view(request, categoria_id=None):
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
        form = forms.form_modificar_categoria(request.POST, request.FILES)
        if form.is_valid():
            if categoria_id:
                categoria = get_object_or_404(
                    Category, pk=categoria_id, empresa=empresa)
                # Verificar si se proporcionó una nueva imagen en el formulario
                if 'image' in form.changed_data:
                    categoria.image = form.cleaned_data['image']
                categoria.description = form.cleaned_data['description']
                categoria.clave = form.cleaned_data['clave']
                categoria.save()
                messages.add_message(request, messages.INFO,
                                     'Categoría modificada con éxito')
                return redirect('mainapp:listar_categorias_view')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Metodo no permitido')
                return redirect('mainapp:listar_categorias_view')
        else:
            return render(request, 'mvcapp/categorias/modificar_categoria.html', {'form': form, 'empresa_pk': empresa.pk})
    else:
        if categoria_id:
            categoria = get_object_or_404(
                Category, pk=categoria_id, empresa=empresa)
            # Asignar la imagen existente al formulario
            form = forms.form_modificar_categoria(
                instance=categoria, initial={'image': categoria.image})
            form.fields['description'].label = 'Descripción de la categoria'
            form.fields['clave'].label = 'Clave de la categoria'
            form.fields['image'].label = 'Imagen de la categoria'
        else:
            form = forms.form_modificar_categoria()

    return render(request, 'mvcapp/categorias/modificar_categoria.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def eliminar_categoria_view(request, categoria_id):
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

    categoria = get_object_or_404(Category, pk=categoria_id, empresa=empresa)

    if request.method == 'POST':
        categoria.delete()
        messages.add_message(request, messages.INFO,
                             'Categoría eliminada con éxito')
        return redirect('mainapp:listar_categorias_view')

    else:
        messages.add_message(request, messages.WARNING, 'Metodo no permitido')
        return redirect('mainapp:listar_categorias_view')

# sin auth para customer


def categorias_customer_view(request, cadena):
    empresa = get_object_or_404(Empresa, nombre_para_pagos=cadena)
    if empresa.horario_de_acceso:
        hora_actual = timezone.localtime(timezone.now()).time()
        hora_inicio = empresa.horario_de_acceso.hora_inicio
        hora_fin = empresa.horario_de_acceso.hora_fin
        if not validar_horario(hora_inicio, hora_fin, hora_actual):    
            messages.add_message(request, messages.WARNING, 'La empresa está fuera de horario')
            return redirect('website:fuera_de_horario', empresa.pk)
    if not empresa.vigente:
        messages.add_message(request, messages.WARNING,
                             'La empresa presenta adeudo y no tiene disponible la sección de pedidos')
        return redirect('administracion:registro')

    categorias = Category.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/categorias/categorias_customers.html',
                  {'categorias': categorias, 'cadena': cadena, 'empresa': empresa})
