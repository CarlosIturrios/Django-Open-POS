# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers

import ast

from mainapp.models import Product
from mainapp.models import Order
from mainapp.models import OrderDetail
from mainapp.models import OrderType
from mainapp.models import Customer
from mainapp.models import Place
from adminapp.models import Empresa
from .index import append_product_to_cart


@login_required()
def orden_cobrada(request, pk):
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
    if 'order' in request.session:
        del request.session['order']
    return render(request, 'mvcapp/ordenes/orden_cobrada.html',
                  {'pk': pk, 'empresa_pk': empresa.pk})


@login_required()
def crear_nueva_orden(request):
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
    if 'order' in request.session:
        messages.add_message(request, messages.ERROR,
                             'Usted cuenta con una orden pendiente, terminela para continuar con una nueva.')
        return redirect('mainapp:categorias')
    tipos_de_orden = OrderType.objects.all()
    places = Place.objects.filter(empresa=empresa)
    if request.method == "POST":
        nueva_orden = Order()
        orden_type = request.POST.get('tipoDeOrden', None)
        place = request.POST.get('place', None)
        comentario = request.POST.get('comentario', None)
        id_cliente = request.POST.get('idCliente', None)
        pago = request.POST.get('pago', None)
        confirmar_orden = request.POST.get('confirmar_orden', None)

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
                    return render(request, 'mvcapp/ordenes/crear_nueva_orden.html', {'tipos_de_orden': tipos_de_orden, 'places': places, 'empresa_pk': empresa.pk})
        else:
            cliente = Customer.objects.get(
                pk=id_cliente, eliminado=False, empresa=empresa)
        nueva_orden.order_type_id = orden_type
        nueva_orden.status_id = 1
        nueva_orden.manager = request.user
        nueva_orden.comments = comentario
        nueva_orden.customer = cliente
        nueva_orden.empresa = empresa
        nueva_orden.place_id = place
        nueva_orden.save()
        if confirmar_orden:
            nueva_orden.status_id = 2
            nueva_orden.waiter = request.user
            nueva_orden.save()
            total = float(0)
            for item in request.session['cart']:
                bandera = True
                for producto in nueva_orden.relacion_Order_a_OrderDetail.all():
                    if producto.product_id == int(item['id_product']):
                        producto.quantity += int(item['cantidad'])
                        producto.observaciones += str(item['observaciones'])
                        producto.save()
                        bandera = False
                        total += (float(producto.product.price)
                                  * float(producto.quantity))
                if bandera:
                    producto = Product.objects.get(
                        pk=item['id_product'], eliminado=False, empresa=empresa)
                    detalle = OrderDetail()
                    detalle.product = producto
                    detalle.quantity = item['cantidad']
                    detalle.observaciones = str(item['observaciones'])
                    detalle.order = nueva_orden
                    detalle.empresa = empresa
                    detalle.save()
                    total += (float(producto.price) * float(detalle.quantity))
            nueva_orden.amount = total
            nueva_orden.save()
            del request.session['cart']
            messages.add_message(request, messages.SUCCESS,
                                 'Orden #{0} creada con exito pedido en cocina'.format(nueva_orden.pk))
            return redirect('mainapp:orden_cobrada', nueva_orden.pk)
        if pago:
            nueva_orden.status_id = 6
            nueva_orden.pagado = True
            nueva_orden.cashier = request.user
            nueva_orden.empresa = empresa
            nueva_orden.save()
            total = float(0)
            for item in request.session['cart']:
                producto = Product.objects.get(
                    pk=item['id_product'], eliminado=False, empresa=empresa)
                detalle = OrderDetail()
                detalle.product = producto
                detalle.quantity = item['cantidad']
                detalle.order = nueva_orden
                detalle.empresa = empresa
                detalle.save()
                total += (float(producto.price) * float(detalle.quantity))
            nueva_orden.amount = total
            nueva_orden.save()
            del request.session['cart']
            messages.add_message(request, messages.SUCCESS,
                                 'Orden #{0} cobrada con exito'.format(nueva_orden.pk))
            return redirect('mainapp:orden_cobrada', nueva_orden.pk)
        request.session['order'] = nueva_orden.pk
        if not cliente:
            messages.add_message(request, messages.SUCCESS,
                                 'Orden sin cliente creada con exito')
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Orden creada con exito')
        return redirect('mainapp:categorias')
    return render(request, 'mvcapp/ordenes/crear_nueva_orden.html', {'tipos_de_orden': tipos_de_orden, 'places': places, 'empresa_pk': empresa.pk})


@login_required()
def detalle_de_la_orden(request):
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
    if request.method == "POST":
        if 'order' in request.session:
            orden = Order.objects.get(
                pk=request.session['order'], eliminado=False, empresa=empresa)
            orden.status_id = 2
            orden.waiter = request.user
            orden.save()
            for item in request.session['cart']:
                bandera = True
                for producto in orden.relacion_Order_a_OrderDetail.all():
                    if producto.product_id == int(item['id_product']):
                        producto.quantity += int(item['cantidad'])
                        #producto.observaciones += str(item['observaciones'])   
                        lista = ast.literal_eval(producto.observaciones)
                        
                        lista.append(str(item['observaciones'][0]))                     
                        producto.observaciones = lista
                        producto.save()
                        bandera = False
                    
                        
                if bandera:
                    producto = Product.objects.get(
                        pk=item['id_product'], eliminado=False, empresa=empresa)
                    detalle = OrderDetail()
                    detalle.product = producto
                    detalle.quantity = item['cantidad']
                    detalle.observaciones = str(item['observaciones'])
                    detalle.order = orden
                    detalle.empresa = empresa
                    detalle.save()           
            detalle = orden.relacion_Order_a_OrderDetail.all()
            total = float(0)
            for item in detalle:
                producto = item.product
                total += float(producto.price) * float(item.quantity)
            orden.amount = total
            orden.save()
            del request.session['cart']
            del request.session['order']
            messages.add_message(request, messages.SUCCESS,
                                 'Orden #{0} actualizada con exito'.format(orden.pk))
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
        messages.add_message(request, messages.ERROR,
                             'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')
    if 'order' in request.session:
        del request.session['order']
    if request.user.groups.filter(name='VENDEDOR').exists():
        ordenes = Order.objects.filter(~Q(status_id=6) & ~Q(status_id=4), pagado=False,
                                       eliminado=False, empresa=empresa)
    if request.user.groups.filter(name='CAJERO').exists():
        ordenes = Order.objects.filter(~Q(status_id=6) & ~Q(status_id=4), pagado=False,
                                       eliminado=False, empresa=empresa)

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

    return render(request, 'mvcapp/ordenes/mis_ordenes.html', {'ordenes': ordenes, 'empresa_pk': empresa.pk})

@login_required()
def mis_ordenes_json(request):
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
    if 'order' in request.session:
        del request.session['order']
    if request.user.groups.filter(name='VENDEDOR').exists():
        ordenes = Order.objects.filter(~Q(status_id=6) & ~Q(status_id=4), pagado=False,
                                       eliminado=False, empresa=empresa)
    if request.user.groups.filter(name='CAJERO').exists():
        ordenes = Order.objects.filter(~Q(status_id=6) & ~Q(status_id=4), pagado=False,
                                       eliminado=False, empresa=empresa)

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

    # Serializar las órdenes en formato JSON
    serialized_ordenes = serializers.serialize('json', ordenes)

    # Devolver la respuesta JSON
    return JsonResponse({'ordenes': serialized_ordenes}, safe=False)

@login_required()
def orden(request, pk):
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
    if request.method == "POST":
        search_content = request.POST.get('q', None)
        cantidad = 1
        if '*' in search_content:
            search_content = search_content.split('*')
            cantidad, search_content = search_content[0], search_content[1]
        productos = Product.objects.filter(Q(barcode=search_content) | Q(name=search_content) | Q(product_code=search_content), empresa=empresa)

        if productos.count() == 1:
            id_product = productos.first().pk
            cantidad = cantidad
            observaciones = None
            # Crear un nuevo diccionario para inyectar valores en el request.POST
            updated_post_data = request.POST.copy()
            updated_post_data['id_product'] = id_product
            updated_post_data['cantidad'] = int(cantidad)
            updated_post_data['observaciones'] = observaciones
            # Actualizar el request.POST con el nuevo diccionario
            request.POST = updated_post_data
            append_product_to_cart(request, empresa, productos.first().category.pk)
            return redirect('mainapp:carrito')
        else: 
            messages.add_message(request, messages.WARNING,
                             'El producto no pudo ser encontrado.')
    orden = Order.objects.get(pk=pk, eliminado=False, empresa=empresa)
    productos = []
    total = float(0)
    pago = None
    if "collection_id" in orden.comments:
        texto_dividido = orden.comments.split("collection_id")
        comentarios = texto_dividido[0]
        print('comentarios: ', len(comentarios))
        pago = texto_dividido[1]
    else:
        comentarios = orden.comments
    request.session['order'] = pk
    for product in orden.relacion_Order_a_OrderDetail.all():
        producto = product.product
        if product.observaciones and product.observaciones !='[][]':
            print(product.observaciones)
            lista_formateada = [elemento.strip().capitalize() if elemento is not None else "Todo incluido" for elemento in eval(product.observaciones)]
        else:
            lista_formateada = ''
        image_url = producto.image.url if producto.image else None
        productos.append({
            'pk': producto.pk,
            'name': producto.name,
            'description': producto.description,
            'quantity': product.quantity,
            'image': image_url,
            'price': float(producto.price),
            'observaciones': '\n'.join([f"- {elemento}" for elemento in lista_formateada]),
            'total': float(producto.price) * product.quantity,
        })
        total += float(producto.price) * product.quantity
        if 'cart' in request.session:
            del request.session['cart']
        if orden.pagado and 'order' in request.session:
            del request.session['order']
    return render(request, 'mvcapp/ordenes/detalle_de_orden.html',
                  {'productos': productos, 'total': total, 'orden': orden, 'pago': pago,
                   'empresa_pk': empresa.pk, 'comentarios': comentarios })


@login_required()
def orden_lista_para_entrega(request, pk):
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

    orden = Order.objects.get(pk=pk, eliminado=False, empresa=empresa)
    orden.cocinado = True
    for detalle in orden.relacion_Order_a_OrderDetail.all():
        producto = detalle.product
        producto.stock -= detalle.quantity
        producto.save()
        for ingrediente in producto.ingredients.all():
            ingrediente.quantity -= detalle.quantity
            ingrediente.save()
    orden.cook = request.user
    orden.status_id = 3
    orden.save()
    messages.add_message(request, messages.SUCCESS,
                         'Orden actualizada con exito.')
    if 'order' in request.session:
        del request.session['order']
    return redirect('mainapp:mis_ordenes')


@login_required()
def orden_entregada(request, pk):
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

    orden = Order.objects.get(pk=pk, eliminado=False, empresa=empresa)
    orden.entregado = True
    orden.dealer = request.user
    orden.status_id = 5
    orden.save()
    messages.add_message(request, messages.SUCCESS,
                         'Orden actualizada con exito.')
    if 'order' in request.session:
        del request.session['order']
    return redirect('mainapp:mis_ordenes')


@login_required()
def listar_ordenes_view(request):
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

    ordenes = Order.objects.filter(eliminado=False, empresa=empresa)
    
    # Obtener los parámetros de consulta de fecha
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    # Establecer el valor predeterminado de los campos de fecha
    if not date1:
        date1 = timezone.localtime(timezone.now())
    if not date2:
        date2 = timezone.localtime(timezone.now())

    # Ensure date1 and date2 are strings
    if isinstance(date1, datetime):
        date1 = date1.strftime('%Y-%m-%d')
    if isinstance(date2, datetime):
        date2 = date2.strftime('%Y-%m-%d')

    fecha_inicial = datetime.strptime(date1, '%Y-%m-%d')
    date1 = fecha_inicial.replace(hour=0, minute=0, second=0)

    # Agregar la hora final (23:59:59) a fecha_final
    fecha_final = datetime.strptime(date2, '%Y-%m-%d')
    date2 = fecha_final.replace(hour=23, minute=59, second=59)

    # Filtrar por rango de fechas si se proporcionan los parámetros de consulta
    if date1 and date2:
        ordenes = ordenes.filter(fecha_de_creacion__range=[date1, date2])
        
    return render(request, 'mvcapp/ordenes/listar_ordenes.html',
                  {'ordenes': ordenes, 'empresa_pk': empresa.pk})

