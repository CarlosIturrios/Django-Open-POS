# -*- coding: utf-8 -*-

from .index import LoginView
from .index import LogoutView
from .index import eliminar_del_carrito_view
from .index import dashboard
from .index import carrito_view
from .index import cobrar
from .index import GeneratePDF

from .lugares import crear_nuevo_place_view
from .lugares import listar_lugares_view
from .lugares import modificar_place_view
from .lugares import eliminar_place_view
from .tipos_de_cantidades import crear_nuevo_quantity_type_view
from .tipos_de_cantidades import listar_tipos_de_cantidades_view
from .tipos_de_cantidades import modificar_quantity_type_view
from .tipos_de_cantidades import eliminar_quantity_type_view
from .ordenes import orden_cobrada
from .ordenes import crear_nueva_orden
from .ordenes import detalle_de_la_orden
from .ordenes import mis_ordenes
from .ordenes import mis_ordenes_json
from .ordenes import orden
from .ordenes import orden_entregada
from .ordenes import orden_lista_para_entrega
from .ordenes import listar_ordenes_view
from .productos import productos_view
from .productos import crear_nuevo_producto_view
from .productos import listar_productos_view
from .productos import modificar_producto_view
from .productos import eliminar_producto_view
from .categorias import categorias_view
from .categorias import crear_nueva_categoria_view
from .categorias import listar_categorias_view
from .categorias import modificar_categoria_view
from .categorias import eliminar_categoria_view
from .monedas import crear_nueva_currency_view
from .monedas import modificar_currency_view
from .monedas import eliminar_moneda_view
from .monedas import listar_monedas_view
from .ingredientes import crear_nuevo_ingredient_view
from .ingredientes import listar_ingredientes_view
from .ingredientes import modificar_ingredient_view
from .ingredientes import eliminar_ingredient_view
from .usuarios import crear_usuario
from .usuarios import modificar_usuario
from .usuarios import listar_usuarios_view
from .clientes import listar_clientes_view

# sin auth para customer

from .categorias import categorias_customer_view
from .productos import productos_customer_view
from .index import carrito_customer_view
from .index import eliminar_del_carrito_customer_view
from .index import crear_nueva_orden_customer_view
from .index import index_customers_view
from .index import orden_pagada_customer_view
from .index import validar_horario
from .index import registro_con_exito
