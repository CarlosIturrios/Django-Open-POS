from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from mainapp.models import Currency
from adminapp.models import Empresa

from mainapp import forms


@login_required()
def listar_monedas_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    monedas = Currency.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/monedas/listar_monedas.html',
                  {'monedas': monedas})


@login_required()
def crear_nueva_currency_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
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
            messages.add_message(request, messages.INFO, 'Moneda agregada con exito')
            return redirect('mainapp:listar_monedas_view')
        else:
            return render(request, 'mvcapp/monedas/crear_currency.html', {'form': form})

    else:
        form = forms.form_agregar_currency()

    return render(request, 'mvcapp/monedas/crear_currency.html', {'form': form})
