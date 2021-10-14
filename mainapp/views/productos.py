from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from mainapp.models import Product
from adminapp.models import Empresa
from mainapp.models import Currency
from mainapp.models import Ingredient
from mainapp.models import Category
from mainapp import forms


@login_required()
def productos_view(request, pk):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    if request.method == "POST":
        id_product = request.POST.get('id_product', None)
        cantidad = request.POST.get('cantidad', None)
        try:
            producto = Product.objects.get(pk=id_product, eliminado=False, empresa=empresa)
        except:
            messages.add_message(request, messages.WARNING, 'Producto no encontrado')
            return redirect('mainapp:productos', pk)
        if 'cart' not in request.session:
            request.session['cart'] = [{'id_product': id_product, 'cantidad': cantidad}]
        else:
            cart = request.session['cart']
            if not any(pro['id_product'] == str(id_product) for pro in cart):
                cart.append({'id_product': id_product, 'cantidad': cantidad})
            else:
                for item in cart:
                    if item['id_product'] == id_product:
                        item['cantidad'] = int(item['cantidad']) + int(cantidad)
            request.session['cantidad'] = cart
        messages.add_message(request, messages.SUCCESS, '{0} agregada a la orden'.format(producto.name))
        return redirect('mainapp:productos', pk)
    productos = Product.objects.filter(category_id=pk, eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/productos/productos.html',
                  {'productos': productos})


@login_required()
def listar_productos_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    productos = Product.objects.filter(eliminado=False, empresa=empresa)
    return render(request, 'mvcapp/productos/listar_productos.html',
                  {'productos': productos})


@login_required()
def crear_nuevo_producto_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')
    monedas = Currency.objects.filter(eliminado=False, empresa=empresa)
    ingredientes = Ingredient.objects.filter(eliminado=False, empresa=empresa)
    categorias = Category.objects.filter(eliminado=False, empresa=empresa)
    if request.method == 'POST':

        form = forms.form_agregar_product(request.POST, request.FILES)

        if form.is_valid():
            producto = form.save(commit=False)
            producto.empresa = empresa

            ingredients = Ingredient.objects.filter(pk__in=request.POST.getlist('ingredients', None), eliminado=False,
                                                    empresa=empresa)
            producto.save()
            for ingredient in ingredients:
                producto.ingredients.add(ingredient)
            messages.add_message(request, messages.INFO, 'Tipo de cantidad agregado con exito')
            return redirect('mainapp:categorias')
        else:
            print(str(form.errors))
            return render(request, 'mvcapp/productos/crear_producto.html',
                          {'form': form, 'monedas': monedas, 'ingredientes': ingredientes, 'categorias': categorias})

    else:
        form = forms.form_agregar_product()

    return render(request, 'mvcapp/productos/crear_producto.html',
                  {'form': form, 'monedas': monedas, 'ingredientes': ingredientes, 'categorias': categorias})
