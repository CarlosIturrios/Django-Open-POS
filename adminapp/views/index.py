from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from adminapp.models import Empresa

from adminapp import forms


@login_required()
def listar_empresas(request):
    request.session['empresa'] = None
    if request.session['empresa'] == None:
        del request.session['empresa']
    empresas = Empresa.objects.filter(
        usuarios=request.user)

    return render(request, 'adminapp/listar_empresas.html', {'empresas': empresas, })


@login_required()
def acceder(request, pk):
    request.session['empresa'] = pk
    return redirect('mainapp:dashboard')


@login_required()
def registrar_empresa(request):
    """ ConfiguracionAgregarEmisor
    Forma para agregar un nuevo emisor al usuario que esta Auth
    """
    if request.method == 'POST':
        empresa = Empresa(cuenta=request.user.relacion_cuenta_de_usuario)
        form = forms.ConfiguracionAgregarEmpresa(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            empresa.usuarios.add(request.user)
            messages.add_message(request, messages.INFO, 'Guardado')
            request.session['empresa'] = empresa.pk
            return redirect('mainapp:dashboard')
        else:
            return render(request, 'adminapp/registrar_empresa.html', {'form': form})
    else:
        form = forms.ConfiguracionAgregarEmpresa()
    return render(request, 'adminapp/registrar_empresa.html', {'form': form})


def registro(request):
    """ registro
    Agregar un usuario totalmente nuevo
    """
    if request.user.is_authenticated:
        return redirect('mainapp:dashboard')
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            correo_del_usuario = form.cleaned_data['email']
            form.save()
            return redirect('mainapp:registro_con_exito', correo_del_usuario=correo_del_usuario)
        else:
            return render(request, 'adminapp/registro.html', {'form': form})
    else:
        form = forms.UserForm()
    return render(request, 'adminapp/registro.html', {'form': form})


@login_required()
def actualizar_empresa(request, empresa_id):
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
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        form = forms.EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                             'Empresa actualizada con exito')
            return redirect('administracion:actualizar_empresa', empresa.pk)
    else:
        form = forms.EmpresaForm(instance=empresa)
        form.fields['nombre_para_pagos'].label = mark_safe(f'<a href="{request.scheme}://{request.get_host()}/app/{empresa.nombre_para_pagos}" target="_blank">Acceso para tus clientes. Click Aquí.</a>')
        form.fields['horario_de_acceso'].label = mark_safe(f'<label for="{{ form.horario_de_acceso.id_for_label }}">Horario de acceso al portal de tus clientes <a data-toggle="modal" data-target="#modal-horario-de-acceso" class="btn btn-block bg-gradient-info btn-xs"> Agregar nuevo </a></label>')

    return render(request, 'adminapp/actualizar_empresa.html', {'form': form, 'empresa': empresa, 'empresa_pk': empresa.pk})