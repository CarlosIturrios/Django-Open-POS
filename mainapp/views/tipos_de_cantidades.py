from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from adminapp.models import Empresa
from mainapp.models import QuantityType

from mainapp import forms


@login_required()
def listar_tipos_de_cantidades_view(request):
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

    tipos_de_cantidades = QuantityType.objects.filter(
        eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/tipos_de_cantidades/listar_cantidades.html',
                  {'tipos_de_cantidades': tipos_de_cantidades, 'empresa_pk': empresa.pk})


@login_required()
def crear_nuevo_quantity_type_view(request):
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

        form = forms.form_agregar_quantity_type(request.POST)
        if form.is_valid():
            quantity = form.save(commit=False)
            quantity.empresa = empresa
            quantity.save()
            messages.add_message(request, messages.INFO,
                                 'Tipo de cantidad agregado con exito')
            return redirect('mainapp:listar_tipos_de_cantidades_view')
        else:
            return render(request, 'mvcapp/tipos_de_cantidades/crear_tipo_de_cantidad.html', {'form': form, 'empresa_pk': empresa.pk})

    else:
        form = forms.form_agregar_quantity_type()
        form.fields['description'].label = 'Descripción de la cantidad'

    return render(request, 'mvcapp/tipos_de_cantidades/crear_tipo_de_cantidad.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def modificar_quantity_type_view(request, quantity_id=None):
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
        form = forms.form_agregar_quantity_type(request.POST)
        if form.is_valid():
            if quantity_id:
                quantity = get_object_or_404(
                    QuantityType, pk=quantity_id, empresa=empresa)

                quantity.description = form.cleaned_data['description']
                quantity.save()
                messages.add_message(request, messages.INFO,
                                     'Tipo de cantidad modificada con éxito')
                return redirect('mainapp:listar_tipos_de_cantidades_view')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Metodo no permitido')
                return redirect('mainapp:listar_tipos_de_cantidades_view')
        else:
            return render(request, 'mvcapp/tipos_de_cantidades/modificar_tipo_de_cantidad.html', {'form': form, 'empresa_pk': empresa.pk})
    else:
        if quantity_id:
            quantity = get_object_or_404(
                QuantityType, pk=quantity_id, empresa=empresa)
            # Asignar la imagen existente al formulario
            form = forms.form_agregar_quantity_type(instance=quantity)
            form.fields['description'].label = 'Descripción de la cantidad'
        else:
            form = forms.form_agregar_quantity_type()

    return render(request, 'mvcapp/tipos_de_cantidades/modificar_tipo_de_cantidad.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def eliminar_quantity_type_view(request, quantity_id=None):
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

    quantity = get_object_or_404(QuantityType, pk=quantity_id, empresa=empresa)

    if request.method == 'POST':
        quantity.delete()
        messages.add_message(request, messages.INFO,
                             'Tipo de cantidad eliminado con éxito')
        return redirect('mainapp:listar_tipos_de_cantidades_view')

    else:
        messages.add_message(request, messages.WARNING, 'Metodo no permitido')
        return redirect('mainapp:listar_tipos_de_cantidades_view')
