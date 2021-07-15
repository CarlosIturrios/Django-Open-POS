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
        messages.add_message(request, messages.SUCCESS, '{0} agregada a la orden    '.format(producto.name))
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
    if 'cart' not in request.session:
        messages.add_message(request, messages.ERROR,
                             'La orden se encuentra vacia, por favor selecciona algunos productos')
        return redirect('mainapp:categorias')
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
        orden = Order()
        orden.status_id = 1
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
                             'Orden cobrada con exito')
        return redirect('mainapp:dashboard')
    else:
        messages.add_message(request, messages.ERROR,
                             'METODO NO PERMITIDO')
        return redirect('mainapp:dashboard')
