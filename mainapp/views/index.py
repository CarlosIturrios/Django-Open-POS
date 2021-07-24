from io import BytesIO
import pdfkit
from django.db.models import Q

from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import views
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Sum

from mainapp.models import Category
from mainapp.models import Product
from mainapp.models import Order
from mainapp.models import OrderDetail
from mainapp.models import OrderType
from mainapp.models import Customer


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'mainapp/template.html'


class LoginView(views.LoginView):
    redirect_authenticated_user = True
    template_name = 'auth/login.html'


class LogoutView(views.LogoutView):
    pass


@login_required()
def categorias_view(request):
    categorias = Category.objects.all()
    return render(request, 'mvcapp/categorias.html',
                  {'categorias': categorias})


@login_required()
def productos_view(request, pk):
    if request.method == "POST":
        id_product = request.POST.get('id_product', None)
        cantidad = request.POST.get('cantidad', None)
        try:
            producto = Product.objects.get(pk=id_product)
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
    productos = Product.objects.filter(category_id=pk)
    return render(request, 'mvcapp/productos.html',
                  {'productos': productos})


@login_required()
def carrito_view(request):
    if 'cart' not in request.session:
        messages.add_message(request, messages.ERROR,
                             'La orden se encuentra vacia, por favor selecciona algunos productos')
        return redirect('mainapp:categorias')
    else:
        productos = []
        total = float(0)
        for item in request.session['cart']:
            producto = Product.objects.get(pk=item['id_product'])
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
    group = Group.objects.get(name='PATRON')
    if not group in request.user.groups.all():
        return redirect('mainapp:categorias')
    ventas_del_dia = Order.objects.all().aggregate(Sum('amount'))
    ventas_del_dia = ventas_del_dia['amount__sum']

    return render(request, 'mvcapp/dashboard.html',
                  {'ventas_del_dia': ventas_del_dia})


def eliminar_del_carrito(request, pk):
    if 'order' in request.session and 'cart' not in request.session:
        order = Order.objects.get(pk=request.session['order'])

        if order.status.pk <= 3:
            detalle = order.relacion_Order_a_OrderDetail.filter(product_id=pk)
            for producto in detalle:
                producto.eliminado = True
                producto.order = None
                producto.save()
            print('si ENTRA AL IF ')
        messages.add_message(request, messages.SUCCESS,
                             'Producto eliminado con exito')
        return redirect('mainapp:carrito')
    if 'cart' not in request.session:
        messages.add_message(request, messages.ERROR,
                             'La orden se encuentra vacia, por favor selecciona algunos productos')
        return redirect('mainapp:categorias')
    if 'order' in request.session:
        order = Order.objects.get(pk=pk)
        if order.status.pk <= 3:
            detalle = order.relacion_Order_a_OrderDetail.get(product_id=pk)
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


def cobrar(request):
    if request.method == "POST":
        if 'cart' not in request.session and 'order' in request.session:
            orden = Order.objects.get(pk=request.session['order'])
            orden.status_id = 6
            orden.cashier = request.user
            orden.save()
            del request.session['order']
        else:
            orden = Order()
            orden.status_id = 6
            orden.cashier = request.user
            orden.save()
            total = float(0)
            for item in request.session['cart']:
                producto = Product.objects.get(pk=item['id_product'])
                detalle = OrderDetail()
                detalle.product = producto
                detalle.quantity = item['cantidad']
                detalle.order = orden
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


def GeneratePDF(request, pk):
    order = Order.objects.get(pk=pk)
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


def orden_cobrada(request, pk):
    return render(request, 'mvcapp/orden_cobrada.html',
                  {'pk': pk})


def crear_nueva_orden(request):
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
                try:
                    cliente.save()
                except Exception as e:
                    messages.add_message(request, messages.ERROR,
                                         'Existe un problema con el cliente {0}'.format(e))
                    return render(request, 'mvcapp/crear_nueva_orden.html', {'tipos_de_orden': tipos_de_orden})
        else:
            cliente = Customer.objects.get(pk=id_cliente)
        nueva_orden.order_type_id = orden_type
        nueva_orden.status_id = 1
        nueva_orden.manager = request.user
        nueva_orden.comments = comentario
        nueva_orden.customer = cliente
        nueva_orden.save()
        request.session['order'] = nueva_orden.pk
        if not cliente:
            messages.add_message(request, messages.SUCCESS, 'Orden sin cliente creada con exito')
        else:
            messages.add_message(request, messages.SUCCESS, 'Orden creada con exito')
        return redirect('mainapp:categorias')
    return render(request, 'mvcapp/crear_nueva_orden.html', {'tipos_de_orden': tipos_de_orden})


def detalle_de_la_orden(request):
    if request.method == "POST":
        if 'order' in request.session:
            orden = Order.objects.get(pk=request.session['order'])
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
                    producto = Product.objects.get(pk=item['id_product'])
                    detalle = OrderDetail()
                    detalle.product = producto
                    detalle.quantity = item['cantidad']
                    detalle.order = orden
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


def mis_ordenes(request):
    ordenes = Order.objects.filter(~Q(status_id=6) & ~Q(status_id=5) & ~Q(status_id=4),
                                   Q(cashier=request.user) | Q(cook=request.user) | Q(waiter=request.user) | Q(
                                       manager=request.user))
    return render(request, 'mvcapp/mis_ordenes.html', {'ordenes': ordenes})


@login_required()
def orden(request, pk):
    orden = Order.objects.get(pk=pk)
    productos = []
    total = float(0)
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
        request.session['order'] = pk
        if 'cart' in request.session:
            del request.session['cart']
    return render(request, 'mvcapp/detalle_de_orden.html',
                  {'productos': productos, 'total': total})
