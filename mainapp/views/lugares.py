from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from adminapp.models import Empresa
from mainapp.models import Place

from mainapp import forms


@login_required()
def listar_lugares_view(request):
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

    lugares = Place.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/lugares/listar_lugares.html',
                  {'lugares': lugares, 'empresa_pk': empresa.pk})


@login_required()
def crear_nuevo_place_view(request):
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

        form = forms.form_agregar_place(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.empresa = empresa
            place.save()
            messages.add_message(request, messages.INFO,
                                 'Lugar agregado con exito')
            return redirect('mainapp:listar_lugares_view')
        else:
            return render(request, 'mvcapp/lugares/crear_lugar.html', {'form': form, 'empresa_pk': empresa.pk})

    else:
        form = forms.form_agregar_place()
        form.fields['description'].label = 'Descripción del lugar'
        form.fields['direction'].label = 'Dirección del lugar'

    return render(request, 'mvcapp/lugares/crear_lugar.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def modificar_place_view(request, place_id=None):
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
        form = forms.form_agregar_place(request.POST)
        if form.is_valid():
            if place_id:
                place = get_object_or_404(
                    Place, pk=place_id, empresa=empresa)

                place.description = form.cleaned_data['description']
                place.direction = form.cleaned_data['direction']
                place.save()
                messages.add_message(request, messages.INFO,
                                     'Lugar modificado con éxito')
                return redirect('mainapp:listar_lugares_view')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Metodo no permitido')
                return redirect('mainapp:listar_lugares_view')
        else:
            return render(request, 'mvcapp/lugares/modificar_lugar.html', {'form': form, 'empresa_pk': empresa.pk})
    else:
        if place_id:
            place = get_object_or_404(
                Place, pk=place_id, empresa=empresa)
            # Asignar la imagen existente al formulario
            form = forms.form_agregar_place(instance=place)
            form.fields['description'].label = 'Descripción del lugar'
            form.fields['direction'].label = 'Dirección del lugar'
        else:
            form = forms.form_agregar_place()

    return render(request, 'mvcapp/lugares/modificar_lugar.html', {'form': form, 'empresa_pk': empresa.pk})


@login_required()
def eliminar_place_view(request, place_id=None):
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

    place = get_object_or_404(Place, pk=place_id, empresa=empresa)

    if request.method == 'POST':
        place.delete()
        messages.add_message(request, messages.INFO,
                             'El lugar se ha eliminado con éxito')
        return redirect('mainapp:listar_lugares_view')

    else:
        messages.add_message(request, messages.WARNING, 'Metodo no permitido')
        return redirect('mainapp:listar_lugares_view')
