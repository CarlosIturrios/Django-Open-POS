# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from mainapp.models import Ingredient
from mainapp.models import QuantityType
from adminapp.models import Empresa

from mainapp import forms


@login_required()
def listar_ingredientes_view(request):
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

    ingredientes = Ingredient.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/ingredientes/listar_ingredientes.html',
                  {'ingredientes': ingredientes, 'empresa_pk': empresa.pk})


@login_required()
def crear_nuevo_ingredient_view(request):
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

        form = forms.form_agregar_ingredient(request.POST, empresa=empresa)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.empresa = empresa
            ingredient.save()
            messages.add_message(request, messages.INFO,
                                 'Ingrediente agregado con exito')
            return redirect('mainapp:listar_ingredientes_view')
        else:
            return render(request, 'mvcapp/ingredientes/crear_ingrediente.html',
                          {'form': form, 'empresa_pk': empresa.pk})

    else:
        form = forms.form_agregar_ingredient(empresa=empresa)

    return render(request, 'mvcapp/ingredientes/crear_ingrediente.html',
                  {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def modificar_ingredient_view(request, pk=None):
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
        form = forms.form_agregar_ingredient(request.POST, empresa=empresa)
        if form.is_valid():
            if pk:
                ingredient = get_object_or_404(
                    Ingredient, pk=pk, empresa=empresa)

                ingredient.name = form.cleaned_data['name']
                ingredient.description = form.cleaned_data['description']
                ingredient.clasification = form.cleaned_data['clasification']
                ingredient.quantity = form.cleaned_data['quantity']
                ingredient.quantity_type = form.cleaned_data['quantity_type']

                ingredient.save()
                messages.add_message(request, messages.INFO,
                                     'Ingrediente modificado con éxito')
                return redirect('mainapp:listar_ingredientes_view')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Metodo no permitido')
                return redirect('mainapp:listar_ingredientes_view')
        else:
            return render(request, 'mvcapp/ingredientes/modificar_ingrediente.html', {'form': form, 'empresa_pk': empresa.pk})
    else:
        if pk:
            ingredient = get_object_or_404(
                Ingredient, pk=pk, empresa=empresa)
            form = forms.form_agregar_ingredient(instance=ingredient, empresa=empresa)
        else:
            form = forms.form_agregar_ingredient(empresa=empresa)

    return render(request, 'mvcapp/ingredientes/modificar_ingrediente.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def eliminar_ingredient_view(request, pk=None):
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

    ingredient = get_object_or_404(Ingredient, pk=pk, empresa=empresa)

    if request.method == 'POST':
        ingredient.delete()
        messages.add_message(request, messages.INFO,
                             'El ingrediente se ha eliminado con éxito')
        return redirect('mainapp:listar_ingredientes_view')

    else:
        messages.add_message(request, messages.WARNING, 'Metodo no permitido')
        return redirect('mainapp:listar_ingredientes_view')
