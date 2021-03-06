from .index import LoginView
from .index import LogoutView
from .index import eliminar_del_carrito
from .index import dashboard
from .index import carrito_view
from .index import cobrar
from .index import GeneratePDF

from .lugares import crear_nuevo_place_view
from .lugares import listar_lugares_view
from .tipos_de_cantidades import crear_nuevo_quantity_type_view
from .tipos_de_cantidades import listar_tipos_de_cantidades_view
from .ordenes import orden_cobrada
from .ordenes import crear_nueva_orden
from .ordenes import detalle_de_la_orden
from .ordenes import mis_ordenes
from .ordenes import orden
from .ordenes import orden_entregada
from .ordenes import orden_lista_para_entrega
from .ordenes import listar_ordenes_view
from .productos import productos_view
from .productos import crear_nuevo_producto_view
from .productos import listar_productos_view
from .categorias import categorias_view
from .categorias import crear_nueva_categoria_view
from .categorias import listar_categorias_view
from .monedas import crear_nueva_currency_view
from .monedas import listar_monedas_view
from .ingredientes import crear_nuevo_ingredient_view
from .ingredientes import listar_ingredientes_view
from .usuarios import crear_usuario
from .usuarios import listar_usuarios_view
from .clientes import listar_clientes_view
