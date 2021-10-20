from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group

from adminapp.models import Empresa

from adminapp import forms


@login_required()
def listar_usuarios_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    usuarios = empresa.usuarios.all()
    return render(request, 'mvcapp/usuarios/listar_usuarios.html',
                  {'usuarios': usuarios})


@login_required()
def crear_usuario(request):
    """ registro
    Agregar un usuario totalmente nuevo
    """
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    grupos = Group.objects.all()
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            my_group = Group.objects.get(name='ADMINISTRADOR')
            my_group.user_set.remove(usuario)
            new_group = Group.objects.get(pk=request.POST.get('grupo', None))
            new_group.user_set.add(usuario)
            empresa.usuarios.add(usuario)
            messages.add_message(request, messages.INFO, 'Usuario agregado con exito')
            return redirect('mainapp:listar_usuarios_view')  # cambia a get de usuarios
        else:
            return render(request, 'mvcapp/usuarios/crear_usuario.html', {'form': form, 'grupos': grupos})
    else:
        form = forms.UserForm()
    return render(request, 'mvcapp/usuarios/crear_usuario.html', {'form': form, 'grupos': grupos})
