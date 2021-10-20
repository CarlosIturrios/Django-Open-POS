from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from mainapp.models import Category
from adminapp.models import Empresa

from mainapp import forms


@login_required()
def listar_categorias_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    categorias = Category.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/categorias/listar_categorias.html',
                  {'categorias': categorias})


@login_required()
def categorias_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    categorias = Category.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/categorias/categorias.html',
                  {'categorias': categorias})


@login_required()
def crear_nueva_categoria_view(request):
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

        form = forms.form_agregar_categoria(request.POST, request.FILES)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.empresa = empresa
            categoria.save()
            messages.add_message(request, messages.INFO, 'Categoria agregada con exito')
            return redirect('mainapp:listar_categorias_view')
        else:
            return render(request, 'mvcapp/categorias/crear_categoria.html', {'form': form})

    else:
        form = forms.form_agregar_categoria()

    return render(request, 'mvcapp/categorias/crear_categoria.html', {'form': form})
