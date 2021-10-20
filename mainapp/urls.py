from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse
from mainapp import views

app_name = 'mainapp'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('loutin/', views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='index'),
    # categorias
    path('categorias/', views.categorias_view, name='categorias'),
    path('agregar-categoria/', views.crear_nueva_categoria_view, name='crear_nueva_categoria_view'),
    path('listar-categorias/', views.listar_categorias_view, name='listar_categorias_view'),
    # monedas
    path('agregar-moneda/', views.crear_nueva_currency_view, name='crear_nueva_currency_view'),
    path('listar-monedas/', views.listar_monedas_view, name='listar_monedas_view'),
    # productos
    path('productos/<int:pk>', views.productos_view, name='productos'),
    path('eliminar-producto/<int:pk>', views.eliminar_del_carrito, name='eliminar_producto'),
    path('agregar-producto/', views.crear_nuevo_producto_view, name='crear_nuevo_producto_view'),
    path('listar-productos/', views.listar_productos_view, name='listar_productos_view'),
    # ordenes
    path('orden/', views.carrito_view, name='carrito'),
    path('cobrar/', views.cobrar, name='cobrar'),
    path('recibo/<int:pk>', views.GeneratePDF, name='recibo'),
    path('orden-cobrada/<int:pk>', views.orden_cobrada, name='orden_cobrada'),
    path('nueva-orden/', views.crear_nueva_orden, name='crear_nueva_orden'),
    path('detalle-de-la-orden/', views.detalle_de_la_orden, name='detalle_de_la_orden'),
    path('mis-ordenes/', views.mis_ordenes, name='mis_ordenes'),
    path('orden/<int:pk>', views.orden, name='orden'),
    path('orden-lista-para-entrega/<int:pk>', views.orden_lista_para_entrega, name='orden_lista_para_entrega'),
    path('orden-entregada/<int:pk>', views.orden_entregada, name='orden_entregada'),
    path('listar-ordenes/', views.listar_ordenes_view, name='listar_ordenes_view'),
    # Lugares
    path('agregar-lugar/', views.crear_nuevo_place_view, name='crear_nuevo_place_view'),
    path('listar-lugares/', views.listar_lugares_view, name='listar_lugares_view'),
    # Ingredientes
    path('agregar-ingrediente/', views.crear_nuevo_ingredient_view, name='crear_nuevo_ingredient_view'),
    path('listar-ingredientes/', views.listar_ingredientes_view, name='listar_ingredientes_view'),
    # usuarios
    path('agregar-nuevo-usuario/', views.crear_usuario, name='crear_usuario'),
    path('listar-usuarios/', views.listar_usuarios_view, name='listar_usuarios_view'),
    # Cantidades
    path('agregar-tipo-de-cantidad/', views.crear_nuevo_quantity_type_view, name='crear_nuevo_quantity_type_view'),
    path('listar-tipos-de-cantidades/', views.listar_tipos_de_cantidades_view, name='listar_tipos_de_cantidades_view'),
    # Clientes
    path('listar-clientes/', views.listar_clientes_view, name='listar_clientes_view'),
]
