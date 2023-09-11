# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from mainapp.models import Currency
from adminapp.models import Empresa

from mainapp import forms


@login_required()
def listar_monedas_view(request):
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

    monedas = Currency.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/monedas/listar_monedas.html',
                  {'monedas': monedas, 'empresa_pk': empresa.pk})


@login_required()
def crear_nueva_currency_view(request):
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
        form = forms.form_agregar_currency(request.POST)
        if form.is_valid():
            currency = form.save(commit=False)
            currency.empresa = empresa
            currency.save()
            messages.add_message(request, messages.INFO,
                                 'Moneda agregada con exito')
            return redirect('mainapp:listar_monedas_view')
        else:
            return render(request, 'mvcapp/monedas/crear_currency.html', {'form': form, 'empresa_pk': empresa.pk})

    else:
        form = forms.form_agregar_currency()
        form.fields['description'].label = 'Descripción de la moneda'
        form.fields['symbol'].label = 'Simbolo de la moneda'

    return render(request, 'mvcapp/monedas/crear_currency.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def modificar_currency_view(request, currency_id):
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
        form = forms.form_agregar_currency(request.POST)
        if form.is_valid():
            if currency_id:
                currency = get_object_or_404(
                    Currency, pk=currency_id, empresa=empresa)

                currency.description = form.cleaned_data['description']
                currency.symbol = form.cleaned_data['symbol']
                currency.save()
                messages.add_message(request, messages.INFO,
                                     'Moneda modificada con éxito')
                return redirect('mainapp:listar_monedas_view')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Metodo no permitido')
                return redirect('mainapp:listar_monedas_view')
        else:
            return render(request, 'mvcapp/monedas/modificar_currency.html', {'form': form, 'empresa_pk': empresa.pk})
    else:
        if currency_id:
            currency = get_object_or_404(
                Currency, pk=currency_id, empresa=empresa)
            # Asignar la imagen existente al formulario
            form = forms.form_agregar_currency(instance=currency)
            form.fields['description'].label = 'Descripción de la moneda'
            form.fields['symbol'].label = 'Simbolo de la moneda'
        else:
            form = forms.form_agregar_currency()
    return render(request, 'mvcapp/monedas/modificar_currency.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def eliminar_moneda_view(request, currency_id):
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

    currency = get_object_or_404(Currency, pk=currency_id, empresa=empresa)

    if request.method == 'POST':
        currency.delete()
        messages.add_message(request, messages.INFO,
                             'Moneda eliminada con éxito')
        return redirect('mainapp:listar_monedas_view')

    else:
        messages.add_message(request, messages.WARNING, 'Metodo no permitido')
        return redirect('mainapp:listar_monedas_view')
