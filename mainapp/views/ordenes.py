from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q

from mainapp.models import Product
from mainapp.models import Order
from mainapp.models import OrderDetail
from mainapp.models import OrderType
from mainapp.models import Customer
from adminapp.models import Empresa


@login_required()
def orden_cobrada(request, pk):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')
    return render(request, 'mvcapp/ordenes/orden_cobrada.html',
                  {'pk': pk})


@login_required()
def crear_nueva_orden(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')
    if 'order' in request.session:
        messages.add_message(request, messages.ERROR,
                             'Usted cuenta con una orden pendiente, terminela para continuar con una nueva.')
        return redirect('mainapp:categorias')
    tipos_de_orden = OrderType.objects.all()
    if request.method == "POST":
        nueva_orden = Order()
        orden_type = request.POST.get('tipoDeOrden', None)
        comentario = request.POST.get('comentario', None)
        id_cliente = request.POST.get('idCliente', None)
        cliente = None
        if id_cliente == None or id_cliente == "":
            cliente_name = request.POST.get('clienteName', None)
            cliente_cellphone = request.POST.get('clienteCellphone', None)
            cliente_direction = request.POST.get('clienteDirection', None)
            cliente_email = request.POST.get('clienteEmail', None)
            if cliente_name != "" and cliente_cellphone != "":
                cliente = Customer()
                cliente.name = cliente_name
                cliente.cellphone = cliente_cellphone
                cliente.direction = cliente_direction
                cliente.email = cliente_email
                cliente.empresa = empresa
                try:
                    cliente.save()
                except Exception as e:
                    messages.add_message(request, messages.ERROR,
                                         'Existe un problema con el cliente {0}'.format(e))
                    return render(request, 'mvcapp/ordenes/crear_nueva_orden.html', {'tipos_de_orden': tipos_de_orden})
        else:
            cliente = Customer.objects.get(pk=id_cliente, eliminado=False, empresa=empresa)
        nueva_orden.order_type_id = orden_type
        nueva_orden.status_id = 1
        nueva_orden.manager = request.user
        nueva_orden.comments = comentario
        nueva_orden.customer = cliente
        nueva_orden.empresa = empresa
        nueva_orden.save()
        request.session['order'] = nueva_orden.pk
        if not cliente:
            messages.add_message(request, messages.SUCCESS, 'Orden sin cliente creada con exito')
        else:
            messages.add_message(request, messages.SUCCESS, 'Orden creada con exito')
        return redirect('mainapp:categorias')
    return render(request, 'mvcapp/ordenes/crear_nueva_orden.html', {'tipos_de_orden': tipos_de_orden})


@login_required()
def detalle_de_la_orden(request):
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
        print(request.session['order'])
        if 'order' in request.session:
            orden = Order.objects.get(pk=request.session['order'], eliminado=False, empresa=empresa)
            orden.status_id = 2
            orden.waiter = request.user
            orden.save()
            total = float(0)
            for item in request.session['cart']:
                bandera = True
                for producto in orden.relacion_Order_a_OrderDetail.all():
                    print(producto.product_id)
                    if producto.product_id == int(item['id_product']):
                        print(item['id_product'], 'entre al if')
                        producto.quantity += int(item['cantidad'])
                        producto.save()
                        bandera = False
                        total += (float(producto.product.price) * float(producto.quantity))
                if bandera:
                    producto = Product.objects.get(pk=item['id_product'], eliminado=False, empresa=empresa)
                    detalle = OrderDetail()
                    detalle.product = producto
                    detalle.quantity = item['cantidad']
                    detalle.order = orden
                    detalle.empresa = empresa
                    detalle.save()
                    total += (float(producto.price) * float(detalle.quantity))
            orden.amount = total
            orden.save()
            del request.session['cart']
            del request.session['order']
            messages.add_message(request, messages.SUCCESS,
                                 'Orden #{0} cobrada con exito'.format(orden.pk))
            return redirect('mainapp:orden_cobrada', orden.pk)
        else:
            messages.add_message(request, messages.ERROR,
                                 'METODO NO PERMITIDO')
            return redirect('mainapp:dashboard')
    else:
        messages.add_message(request, messages.ERROR,
                             'No existe una orden para asignar.')
        return redirect('mainapp:crear_nueva_orden')


@login_required()
def mis_ordenes(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    if request.user.groups.filter(name='CAJERO').exists():
        ordenes = Order.objects.filter(~Q(status_id=6) & ~Q(status_id=5) & ~Q(status_id=4), pagado=False,
                                       eliminado=False,
                                       empresa=empresa)

    elif request.user.groups.filter(name='COCINERO').exists():
        ordenes = Order.objects.filter(~Q(status_id=5) & ~Q(status_id=4), Q(cook=None) | Q(cook=request.user),
                                       cocinado=False, eliminado=False, empresa=empresa)
    elif request.user.groups.filter(name='REPARTIDOR').exists():
        ordenes = Order.objects.filter(~Q(status_id=5) & ~Q(status_id=4), Q(dealer=None) | Q(dealer=request.user),
                                       entregado=False, cocinado=True, eliminado=False, empresa=empresa)
    elif request.user.groups.filter(name='MESERO').exists():
        ordenes = Order.objects.filter(~Q(status_id=6) & ~Q(status_id=5) & ~Q(status_id=4), pagado=False,
                                       waiter=request.user, eliminado=False, empresa=empresa)
    else:
        ordenes = Order.objects.filter(eliminado=False, empresa=empresa)

    return render(request, 'mvcapp/ordenes/mis_ordenes.html', {'ordenes': ordenes})


@login_required()
def orden(request, pk):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')
    orden = Order.objects.get(pk=pk, eliminado=False, empresa=empresa)
    productos = []
    total = float(0)
    request.session['order'] = pk
    for product in orden.relacion_Order_a_OrderDetail.all():
        producto = product.product
        productos.append({
            'pk': producto.pk,
            'name': producto.name,
            'description': producto.description,
            'quantity': product.quantity,
            'image': producto.image.url,
            'price': float(producto.price),
            'total': float(producto.price) * product.quantity,
        })
        total += float(producto.price) * product.quantity
        if 'cart' in request.session:
            del request.session['cart']
    print(request.session['order'])
    return render(request, 'mvcapp/ordenes/detalle_de_orden.html',
                  {'productos': productos, 'total': total, 'orden': orden})


@login_required()
def orden_lista_para_entrega(request, pk):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    orden = Order.objects.get(pk=pk, eliminado=False, empresa=empresa)
    orden.cocinado = True
    orden.cook = request.user
    orden.status_id = 3
    orden.save()
    messages.add_message(request, messages.SUCCESS,
                         'Orden actualizada con exito.')
    return redirect('mainapp:mis_ordenes')


@login_required()
def orden_entregada(request, pk):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')

    orden = Order.objects.get(pk=pk, eliminado=False, empresa=empresa)
    orden.entregado = True
    orden.dealer = request.user
    orden.status_id = 5
    orden.save()
    messages.add_message(request, messages.SUCCESS,
                         'Orden actualizada con exito.')
    return redirect('mainapp:mis_ordenes')
