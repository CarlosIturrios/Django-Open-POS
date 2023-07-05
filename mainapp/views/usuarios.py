from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from adminapp.models import Empresa

from adminapp import forms


@login_required()
def listar_usuarios_view(request):
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

    usuarios = empresa.usuarios.all()
    return render(request, 'mvcapp/usuarios/listar_usuarios.html',
                  {'usuarios': usuarios, 'empresa_pk': empresa.pk})


@login_required()
def crear_usuario(request):
    """ registro
    Agregar un usuario totalmente nuevo
    """
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

    grupos = Group.objects.exclude(pk=5)
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            usuario.groups.clear()

        # Agregar nuevos grupos seleccionados
            grupos_seleccionados = request.POST.getlist('grupos')
            for grupo_id in grupos_seleccionados:
                grupo = Group.objects.get(pk=grupo_id)
                grupo.user_set.add(usuario)
            empresa.usuarios.add(usuario)
            messages.add_message(request, messages.INFO,
                                 'Usuario agregado con exito')
            # cambia a get de usuarios
            return redirect('mainapp:listar_usuarios_view')
        else:
            return render(request, 'mvcapp/usuarios/crear_usuario.html', {'form': form, 'grupos': grupos, 'empresa_pk': empresa.pk})
    else:
        form = forms.UserForm()
    return render(request, 'mvcapp/usuarios/crear_usuario.html', {'form': form, 'grupos': grupos, 'empresa_pk': empresa.pk})


@login_required
def modificar_usuario(request, pk):
    """ registro
    Agregar un usuario totalmente nuevo
    """
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
    user = User.objects.get(pk=pk)

    if request.method == 'POST':
        form = forms.UserUpdateForm(request.POST, instance=user)
        if form.is_valid():

            form.save()

            # Actualizar grupos de usuario si es necesario
            grupos_seleccionados = request.POST.getlist('groups')
            user.groups.clear()  # Eliminar todos los grupos existentes
            user.groups.add(*grupos_seleccionados) 

            messages.success(request, 'Usuario modificado exitosamente.')
            return redirect('mainapp:listar_usuarios_view')  # Cambia 'perfil' por la URL de tu vista de perfil de usuario
    else:
        form = forms.UserUpdateForm(instance=user)

    return render(request, 'mvcapp/usuarios/modificar_usuario.html', {'form': form, 'empresa_pk': empresa.pk})