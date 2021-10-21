import pdfkit
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
from mainapp.models import Customer
from adminapp.models import Empresa


class LoginView(views.LoginView):
    redirect_authenticated_user = True
    template_name = 'auth/login.html'


class LogoutView(views.LogoutView):
    pass


@login_required()
def carrito_view(request):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
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
        productos = []
        total = float(0)
        for item in request.session['cart']:
            producto = Product.objects.get(pk=item['id_product'], eliminado=False, empresa=empresa)
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
        return render(request, 'mvcapp/carrito.html',
                      {'productos': productos, 'total': total})


@login_required()
def dashboard(request):
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
                                                  fecha_de_creacion__range=[fecha_inicial, fecha_final],
                                                  eliminado=False, empresa=empresa)
    else:
        ventas_del_dia = Order.objects.filter(pagado=True, eliminado=False, empresa=empresa).aggregate(Sum('amount'))
        clientes_nuevos = Customer.objects.filter(eliminado=False, empresa=empresa)
        ordenes_vendidas = Order.objects.filter(pagado=True, eliminado=False, empresa=empresa)
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
                   'ordenes_vendidas': ordenes_vendidas})


@login_required()
def eliminar_del_carrito(request, pk):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')
    if 'order' in request.session and 'cart' not in request.session:
        order = Order.objects.get(pk=request.session['order'], eliminado=False, empresa=empresa)

        if order.status.pk <= 3:
            detalle = order.relacion_Order_a_OrderDetail.filter(product_id=pk, eliminado=False, empresa=empresa)
            for producto in detalle:
                producto.eliminado = True
                producto.order = None
                producto.save()
        messages.add_message(request, messages.SUCCESS,
                             'Producto eliminado con exito')
        return redirect('mainapp:carrito')
    if 'cart' not in request.session:
        messages.add_message(request, messages.ERROR,
                             'La orden se encuentra vacia, por favor selecciona algunos productos')
        return redirect('mainapp:categorias')
    if 'order' in request.session:
        order = Order.objects.get(pk=pk, eliminado=False, empresa=empresa)
        if order.status.pk <= 3:
            detalle = order.relacion_Order_a_OrderDetail.get(product_id=pk, eliminado=False, empresa=empresa)
            detalle.delete()
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
        return redirect('mainapp:carrito')


@login_required()
def cobrar(request):
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
        if 'cart' not in request.session and 'order' in request.session:
            orden = Order.objects.get(pk=request.session['order'], eliminado=False, empresa=empresa)
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
        messages.add_message(request, messages.SUCCESS,
                             'Orden #{0} cobrada con exito'.format(orden.pk))
        return redirect('mainapp:orden_cobrada', orden.pk)
    else:
        messages.add_message(request, messages.ERROR,
                             'METODO NO PERMITIDO')
        return redirect('mainapp:dashboard')


@login_required()
def GeneratePDF(request, pk):
    if not 'empresa' in request.session:
        messages.add_message(request, messages.ERROR, 'Tiene que acceder con una empresa.')
        return redirect('administracion:listar_empresas')
    else:
        empresa = Empresa.objects.get(pk=request.session['empresa'])
        if not empresa.vigente:
            messages.add_message(request, messages.WARNING,
                                 'La empresa presenta un adeudo, comuniquese con el administrador del portal')
            return redirect('administracion:listar_empresas')
    order = Order.objects.get(pk=pk, eliminado=False, empresa=empresa)
    detalle = order.relacion_Order_a_OrderDetail.all()
    productos = []

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
    html = get_template('mvcapp/recibo.html').render({'order': order, 'productos': productos})

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'quiet': '',
    }

    output = pdfkit.from_string(html, False, options=options)
    response = HttpResponse(content_type="application/pdf")
    response.write(output)
    return response
