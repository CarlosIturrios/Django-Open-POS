# -*- coding: utf-8 -*-
import sys
import uuid
from django.contrib.auth.models import Group
import pdfkit
import mercadopago

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import views
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models import Q

from mainapp.models import Product
from mainapp.models import Order
from mainapp.models import OrderDetail
from mainapp.models import OrderType
from mainapp.models import Customer
from mainapp.models import Place
from adminapp.models import Empresa
from adminapp.models import PaymentWithMercadoPago


class LoginView(views.LoginView):
    redirect_authenticated_user = True
    template_name = 'auth/login.html'


class LogoutView(views.LogoutView):
    pass


@login_required()
def carrito_view(request):
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
    if 'cart' not in request.session:
        messages.add_message(request, messages.ERROR,
                             'La orden se encuentra vacia, por favor selecciona algunos productos')
        return redirect('mainapp:categorias')
    else:
        productos, total, tipos_de_orden, places = consulta_carrito(request, empresa)
        return render(request, 'mvcapp/carrito.html',
                      {'productos': productos, 'total': total, 'tipos_de_orden': tipos_de_orden, 'places': places,'empresa_pk': empresa.pk})


@login_required()
def dashboard(request):
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
        fecha_inicial = request.POST.get('date1', None)
        fecha_final = request.POST.get('date2', None)

        ventas_del_dia = Order.objects.filter(fecha_de_creacion__range=[fecha_inicial, fecha_final], pagado=True,
                                              eliminado=False,
                                              empresa=empresa).aggregate(Sum('amount'))
        clientes_nuevos = Customer.objects.filter(fecha_de_creacion__range=[fecha_inicial, fecha_final],
                                                  eliminado=False, empresa=empresa)
        ordenes_vendidas = Order.objects.filter(fecha_de_creacion__range=[fecha_inicial, fecha_final],
                                                pagado=True, eliminado=False, empresa=empresa)
        ordenes_pendientes = Order.objects.filter(Q(pagado=False) | Q(cocinado=False) | Q(entregado=False),
                                                  fecha_de_creacion__range=[
                                                      fecha_inicial, fecha_final],
                                                  eliminado=False, empresa=empresa)
    else:
        ventas_del_dia = Order.objects.filter(
            pagado=True, eliminado=False, empresa=empresa).aggregate(Sum('amount'))
        clientes_nuevos = Customer.objects.filter(
            eliminado=False, empresa=empresa)
        ordenes_vendidas = Order.objects.filter(
            pagado=True, eliminado=False, empresa=empresa)
        ordenes_pendientes = Order.objects.filter(Q(pagado=False) | Q(cocinado=False) | Q(entregado=False),
                                                  eliminado=False, empresa=empresa)
    ventas_del_dia = ventas_del_dia['amount__sum']
    clientes_nuevos = clientes_nuevos.count()
    ordenes_vendidas = ordenes_vendidas.count()
    ordenes_pendientes = ordenes_pendientes.count()

    ventas_del_dia = 0 if ventas_del_dia == None else ventas_del_dia

    return render(request, 'mvcapp/dashboard.html',
                  {'ventas_del_dia': ventas_del_dia, 'clientes_nuevos': clientes_nuevos,
                   'ordenes_pendientes': ordenes_pendientes,
                   'ordenes_vendidas': ordenes_vendidas, 'empresa_pk': empresa.pk})


@login_required()
def eliminar_del_carrito_view(request, pk):
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
    confirmacion = eliminar_del_carrito(request, pk, empresa)
    if not confirmacion:
        return redirect('mainapp:carrito')
    else:
        messages.add_message(request, messages.ERROR,
                             'La orden se encuentra vacia, por favor selecciona algunos productos')
        return redirect('mainapp:categorias')


@login_required()
def cobrar(request):
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
        if 'cart' not in request.session and 'order' in request.session:
            orden = Order.objects.get(
                pk=request.session['order'], eliminado=False, empresa=empresa)
            orden.status_id = 6
            orden.pagado = True
            orden.cashier = request.user
            orden.save()
            del request.session['order']
        else:
            orden = Order()
            orden.status_id = 6
            orden.pagado = True
            orden.cashier = request.user
            orden.empresa = empresa
            orden.save()
            total = float(0)
            for item in request.session['cart']:
                producto = Product.objects.get(
                    pk=item['id_product'], eliminado=False, empresa=empresa)
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
        messages.add_message(request, messages.SUCCESS,
                             'Orden #{0} cobrada con exito'.format(orden.pk))
        return redirect('mainapp:orden_cobrada', orden.pk)
    else:
        messages.add_message(request, messages.ERROR,
                             'METODO NO PERMITIDO')
        return redirect('mainapp:dashboard')


# no auth
def GeneratePDF(request, pk):
    order = Order.objects.get(pk=pk, eliminado=False)
    detalle = order.relacion_Order_a_OrderDetail.all()
    productos = []
    total = float(0)
    for item in detalle:
        producto = item.product
        productos.append({
            'pk': producto.pk,
            'name': producto.name,
            'description': producto.description,
            'quantity': item.quantity,
            'image': producto.image.url,
            'price': float(producto.price),
            'total': float(producto.price) * float(item.quantity),
        })
        total += float(producto.price) * float(item.quantity)
    html = get_template(
        'mvcapp/recibo.html').render({'order': order, 'total': total, 'productos': productos})

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'quiet': '',
    }

    output = pdfkit.from_string(html, False, options=options)
    response = HttpResponse(content_type="application/pdf")
    response.write(output)
    return response

# sin auth para customer


def carrito_customer_view(request, cadena):
    empresa = get_object_or_404(Empresa, nombre_para_pagos=cadena)
    if not empresa.vigente:
        messages.add_message(request, messages.WARNING,
                             'La empresa presenta adeudo y no tiene disponible la sección de pedidos')
        return redirect('administracion:registro')

    if 'cart' not in request.session:
        messages.add_message(request, messages.ERROR,
                             'La orden se encuentra vacia, por favor selecciona algunos productos')
        return redirect('mainapp:categorias_customer_view', cadena)
    else:
        sdk = None
        preference = None
        productos= None
        total = None 
        tipos_de_orden = None
        places = None
        if empresa.sdk_public and empresa.sdk_private:
            sdk = mercadopago.SDK(empresa.sdk_private)
            productos, total, tipos_de_orden, places = consulta_carrito(request, empresa)
            # Crea un ítem en la preferencia
            items = []
            #webhook = f'{request.scheme}://{request.get_host()}/api/webhooks/mercado-pago'
            for producto in productos:
                items.append({
                    "id": producto['pk'],
                    "title": producto['name'],
                    "quantity": int(producto['quantity']),
                    "unit_price": producto['price'],
                })
                
            url = request.build_absolute_uri()
            
            uuid_obj = uuid.uuid4()
            short_uuid = uuid_obj.hex[:11]
            preference_data = {
                "items": items,
                "back_urls": {
                    "success": url,
                    "failure": url,
                    "pending": url
                },
                "auto_return": "approved",
                "payment_methods": {
                    "excluded_payment_types": [
                        {
                            "id": "ticket",
                            "id": "bank_transfer"}
                    ],
                },
                 #webhook, 
                #"statement_descriptor": empresa.nombre_comercial,
                "external_reference": short_uuid,
            }
            
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]
            if 'nueva_orden' in request.session: 
                request.session['nueva_orden']['sdk'] = preference
                nueva_orden = request.session['nueva_orden']
                try:                    
                    pago = PaymentWithMercadoPago.objects.get(payment_id=request.session['nueva_orden']['sdk']['id'])
                except:    
                    pago = PaymentWithMercadoPago()
                    pago.user_id = nueva_orden['sdk']['collector_id']
                pago.payment_id = nueva_orden['sdk']['id']
                pago.nueva_orden = nueva_orden
                pago.coupon_code = nueva_orden['sdk']['coupon_code']
                pago.coupon_labels = nueva_orden['sdk']['coupon_labels']
                pago.date_created = nueva_orden['sdk']['date_created']
                pago.date_of_expiration = nueva_orden['sdk']['date_of_expiration']
                pago.expiration_date_from = nueva_orden['sdk']['expiration_date_from']
                pago.expiration_date_to = nueva_orden['sdk']['expiration_date_to']
                pago.expires = nueva_orden['sdk']['expires']                
                pago.external_reference = short_uuid
                pago.init_point = nueva_orden['sdk']['init_point']
                pago.internal_metadata = nueva_orden['sdk']['internal_metadata']
                pago.items = nueva_orden['sdk']['items']
                pago.save()
        return render(request, 'mvcapp/carrito_customers.html',
                      {'productos': productos, 'total': total, 'tipos_de_orden': tipos_de_orden, 'places': places, 'cadena': cadena, 
                       'preference': preference, 'empresa': empresa})

# sin auth para customer


def eliminar_del_carrito_customer_view(request, pk, cadena):
    empresa = get_object_or_404(Empresa, nombre_para_pagos=cadena)
    if not empresa.vigente:
        messages.add_message(request, messages.WARNING,
                             'La empresa presenta adeudo y no tiene disponible la sección de pedidos')
        return redirect('administracion:registro')

    confirmacion = eliminar_del_carrito(request, pk, empresa, cadena)
    if confirmacion:
        return redirect('mainapp:carrito_customer_view', cadena)
    else:
        messages.add_message(request, messages.ERROR,
                             'La orden se encuentra vacia, por favor selecciona algunos productos')
        return redirect('mainapp:categorias_customer_view', cadena)


def consulta_carrito(request, empresa):
    tipos_de_orden = OrderType.objects.all()
    places = Place.objects.filter(empresa=empresa)
    productos = []
    total = float(0)
    for item in request.session['cart']:
        try:
            producto = Product.objects.get(
                pk=item['id_product'], eliminado=False, empresa=empresa)
        except:
            del request.session['cart']
            messages.add_message(request, messages.WARNING, 'Sucedio algo extraño con su orden. Disculpanos vuelve a iniciar.')
            return productos, total, tipos_de_orden, redirect('mainapp:categorias_customer_view', empresa.nombre_para_pagos)
        productos.append({
            'pk': producto.pk,
            'name': producto.name,
            'description': producto.description,
            'quantity': item['cantidad'],
            'image': producto.image.url,
            'price': float(producto.price),
            'total': float(producto.price) * float(item['cantidad']),
        })
        total += float(producto.price) * float(item['cantidad'])
    return productos, total, tipos_de_orden, places


def eliminar_del_carrito(request, pk, empresa, cadena=None):

    if 'order' in request.session and 'cart' not in request.session:
        order = Order.objects.get(
            pk=request.session['order'], eliminado=False, empresa=empresa)

        if order.status.pk <= 3:
            detalle = order.relacion_Order_a_OrderDetail.filter(
                product_id=pk, eliminado=False, empresa=empresa)
            for producto in detalle:
                producto.eliminado = True
                producto.order = None
                producto.save()
        messages.add_message(request, messages.SUCCESS,
                             'Producto eliminado con exito')
    if 'cart' not in request.session:
        messages.add_message(request, messages.ERROR,
                             'La orden se encuentra vacia, por favor selecciona algunos productos')
        return redirect('mainapp:categorias')

    if 'order' in request.session:
        order = Order.objects.get(pk=pk, eliminado=False, empresa=empresa)
        if order.status.pk <= 3:
            detalle = order.relacion_Order_a_OrderDetail.get(
                product_id=pk, eliminado=False, empresa=empresa)
            detalle.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Producto eliminado con exito')
    else:
        for i in range(len(request.session['cart'])):
            if request.session['cart'][i]['id_product'] == str(pk):
                del request.session['cart'][i]
                break
        request.session['cart'] = request.session['cart']
        if len(request.session['cart']) == 0:
            request.session['cart'] = []
        messages.add_message(request, messages.SUCCESS,
                             'Producto eliminado con exito')
    if not cadena:
        return False
    else:
        return True


def crear_nueva_orden_customer_view(request, cadena):
    empresa = get_object_or_404(Empresa, nombre_para_pagos=cadena)
    if not empresa.vigente:
        messages.add_message(request, messages.WARNING,
                             'La empresa presenta adeudo y no tiene disponible la sección de pedidos')
        return redirect('administracion:registro')

    if request.method == "POST":
        pago = request.POST.get('pago', None)
        data_id = request.POST.get('payment_id', None)
        try:
            payment_mp = PaymentWithMercadoPago.objects.get(data_id=data_id, pagado=False)
        except:
            payment_mp = None
        if payment_mp is not None:
            if 'nueva_orden' in request.session:
                del request.session['nueva_orden']
            nueva_orden_data = payment_mp.nueva_orden
            nueva_orden = Order()
            nueva_orden.PaymentWithMercadoPago = payment_mp
            payment_mp.pagado = True
            payment_mp.save()
            nueva_orden.order_type_id = nueva_orden_data.get(
                'orden_type', None)
            nueva_orden.place_id = nueva_orden_data.get(
                'place', None)
            nueva_orden.status_id = nueva_orden_data.get('status_id', None)
            nueva_orden.waiter_id = nueva_orden_data.get('waiter', None)
            nueva_orden.empresa_id = nueva_orden_data.get('empresa', None)
            comentario = nueva_orden_data.get('comentario', None)
            id_cliente = nueva_orden_data.get('id_cliente', None)

            cliente = None
            if id_cliente == None or id_cliente == "":
                cliente_name = nueva_orden_data["cliente"].get(
                    'cliente_name', None)
                cliente_cellphone = nueva_orden_data["cliente"].get(
                    'cliente_cellphone', None)
                cliente_direction = nueva_orden_data["cliente"].get(
                    'cliente_direction', None)
                cliente_email = nueva_orden_data["cliente"].get(
                    'cliente_email', None)
                if cliente_name and cliente_cellphone:
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
                        return redirect('mainapp:carrito_customer_view', cadena)
            else:
                cliente = Customer.objects.get(
                    pk=id_cliente, eliminado=False, empresa=empresa)

            nueva_orden.manager_id = nueva_orden_data.get('waiter', None)
            nueva_orden.comments = comentario
            nueva_orden.customer = cliente
            nueva_orden.save()

# Resto de tu código

        # has esta logica y saca toda la info de request.session['client'] en lugar de el form post
            total = float(0)
            for item in request.session['cart']:
                bandera = True
                for producto in nueva_orden.relacion_Order_a_OrderDetail.all():
                    if producto.product_id == int(item['id_product']):
                        producto.quantity += int(item['cantidad'])
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
                    detalle.order = nueva_orden
                    detalle.empresa = empresa
                    detalle.save()
                    total += (float(producto.price) *
                            float(detalle.quantity))
            nueva_orden.amount = total
            nueva_orden.save()
            del request.session['cart']
            if pago:
                nueva_orden.status_id = 6
                nueva_orden.pagado = True
                nueva_orden.cashier_id = nueva_orden_data.get('waiter', None)
                nueva_orden.comments += str(
                    request.POST.get('comentario', None),)
                nueva_orden.save()
                total = float(0)
                messages.add_message(request, messages.SUCCESS,
                                    'Orden #{0} cobrada con exito'.format(nueva_orden.pk))
            request.session['order'] = nueva_orden.pk
            #del request.session['nueva_orden']
            if not cliente:
                messages.add_message(request, messages.SUCCESS,
                                    'Orden sin cliente creada con exito')
            else:
                messages.add_message(request, messages.SUCCESS,
                                    'Orden creada con exito')
            return redirect('mainapp:orden_pagada_customer_view', cadena, nueva_orden.pk)
    
        else:
            # crea el objeto client en la request sesión con la logica de arriba aqui si guarda todo lo del post
            grupo_administrador = Group.objects.get(name='ADMINISTRADOR')
            usuario_administrador = grupo_administrador.user_set.first()

            nueva_orden = {
                "orden_type": request.POST.get('tipoDeOrden', None),
                "place": request.POST.get('place', None),
                "comentario": request.POST.get('comentario', None),
                "id_cliente": request.POST.get('idCliente', None),
                "status_id": 2,
                "waiter": usuario_administrador.pk,
                "empresa": empresa.pk,
                "sdk": None,
                "cliente": {}
            }
    
            if nueva_orden["id_cliente"] == None or nueva_orden["id_cliente"] == "":
                nueva_orden["cliente"]["cliente_name"] = request.POST.get(
                    'clienteName', None)
                nueva_orden["cliente"]["cliente_cellphone"] = request.POST.get(
                    'clienteCellphone', None)
                nueva_orden["cliente"]["cliente_direction"] = request.POST.get(
                    'clienteDirection', None)
                nueva_orden["cliente"]["cliente_email"] = request.POST.get(
                    'clienteEmail', None)
            else:
                cliente = Customer.objects.get(
                    pk=nueva_orden["id_cliente"], eliminado=False, empresa=empresa)

            request.session['nueva_orden'] = nueva_orden

            return redirect('mainapp:carrito_customer_view', cadena)
    return redirect('mainapp:carrito_customer_view', cadena)


def index_customers_view(request, cadena):
    empresa = get_object_or_404(Empresa, nombre_para_pagos=cadena)
    if not empresa.vigente:
        messages.add_message(request, messages.WARNING,
                             'La empresa presenta adeudo y no tiene disponible la sección de pedidos')
        return redirect('administracion:registro')

    return render(request, 'mvcapp/clientes/index_customers.html', {'cadena': cadena, 'empresa': empresa})


def orden_pagada_customer_view(request, cadena, pk):
    empresa = get_object_or_404(Empresa, nombre_para_pagos=cadena)
    if not empresa.vigente:
        messages.add_message(request, messages.WARNING,
                             'La empresa presenta adeudo y no tiene disponible la sección de pedidos')
        return redirect('administracion:registro')
    orden = get_object_or_404(Order, pk=pk, empresa=empresa)
    
    return render(request, 'mvcapp/clientes/orden_pagada_customers.html', {'cadena': cadena, 'pk': pk, 'orden': orden, 'empresa': empresa})
