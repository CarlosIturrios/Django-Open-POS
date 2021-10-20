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
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    ingredientes = Ingredient.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/ingredientes/listar_ingredientes.html',
                  {'ingredientes': ingredientes})


@login_required()
def crear_nuevo_ingredient_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')
    quantity_types = QuantityType.objects.filter(eliminado=False, empresa=empresa)
    if request.method == 'POST':

        form = forms.form_agregar_ingredient(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.empresa = empresa
            place.save()
            messages.add_message(request, messages.INFO, 'Ingrediente agregado con exito')
            return redirect('mainapp:listar_ingredientes_view')
        else:
            return render(request, 'mvcapp/ingredientes/crear_ingrediente.html',
                          {'form': form, 'quantity_types': quantity_types})

    else:
        form = forms.form_agregar_ingredient()

    return render(request, 'mvcapp/ingredientes/crear_ingrediente.html',
                  {'form': form, 'quantity_types': quantity_types})
