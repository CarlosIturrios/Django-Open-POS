from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from adminapp.models import Empresa
from mainapp.models import QuantityType

from mainapp import forms


@login_required()
def listar_tipos_de_cantidades_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    tipos_de_cantidades = QuantityType.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/tipos_de_cantidades/listar_cantidades.html',
                  {'tipos_de_cantidades': tipos_de_cantidades})


@login_required()
def crear_nuevo_quantity_type_view(request):
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

        form = forms.form_agregar_quantity_type(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.empresa = empresa
            place.save()
            messages.add_message(request, messages.INFO, 'Tipo de cantidad agregado con exito')
            return redirect('mainapp:categorias')
        else:
            return render(request, 'mvcapp/tipos_de_cantidades/crear_tipo_de_cantidad.html', {'form': form})

    else:
        form = forms.form_agregar_quantity_type()

    return render(request, 'mvcapp/tipos_de_cantidades/crear_tipo_de_cantidad.html', {'form': form})
