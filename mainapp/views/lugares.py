from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from adminapp.models import Empresa
from mainapp.models import Place

from mainapp import forms


@login_required()
def listar_lugares_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    lugares = Place.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/lugares/listar_lugares.html',
                  {'lugares': lugares})


@login_required()
def crear_nuevo_place_view(request):
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

        form = forms.form_agregar_place(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.empresa = empresa
            place.save()
            messages.add_message(request, messages.INFO, 'Lugar agregado con exito')
            return redirect('mainapp:categorias')
        else:
            return render(request, 'mvcapp/lugares/crear_lugar.html', {'form': form})

    else:
        form = forms.form_agregar_place()

    return render(request, 'mvcapp/lugares/crear_lugar.html', {'form': form})
