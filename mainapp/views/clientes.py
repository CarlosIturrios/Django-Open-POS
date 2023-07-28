from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect

from mainapp.models import Customer
from adminapp.models import Empresa


@login_required()
def listar_clientes_view(request):
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

    clientes = Customer.objects.filter(eliminado=False, empresa=empresa)

    # Obtener los parámetros de consulta de fecha
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')

    # Establecer el valor predeterminado de los campos de fecha
    if not date1:
        date1 = timezone.localtime(timezone.now())
    if not date2:
        date2 = timezone.localtime(timezone.now())

    # Filtrar por rango de fechas si se proporcionan los parámetros de consulta
    if date1 and date2:
        clientes = clientes.filter(fecha_de_creacion__range=[date1, date2])
    return render(request, 'mvcapp/clientes/listar_clientes.html',
                  {'clientes': clientes, 'empresa_pk': empresa.pk})


@login_required()
def agregar_clientes_view(request):
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

    clientes = Customer.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/clientes/listar_clientes.html',
                  {'clientes': clientes, 'empresa_pk': empresa.pk})
