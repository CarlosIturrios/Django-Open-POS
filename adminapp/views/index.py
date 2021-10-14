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
            form.save()
            return redirect('mainapp:login')
        else:
            return render(request, 'adminapp/registro.html', {'form': form})
    else:
        form = forms.UserForm()
    return render(request, 'adminapp/registro.html', {'form': form})
